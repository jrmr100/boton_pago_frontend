from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.pagomovil_bp.templates.form_fields import FormFields
from src.utils.api_vippo import leer_listabancos, validar_pago
from src.utils.api_mw import buscar_facturas, pagar_facturas
from src.utils.logger import logger
from flask_login import login_required
import src.config as config

nombre_ruta = "pagomovil"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)

# Cargo la lista de bancos solo una vez cuando se acceda a la ruta pagomovil
listabancos = None

@blue_ruta.before_request
def cargar_listabancos():
    global listabancos
    if listabancos is None:
        listabancos = leer_listabancos()
        # Carga de los bancos emisores al selectfield ENTITY
        if "error listabancos" in listabancos:
            logger.error("Error obteniendo la lista de bancos desde el archivo TXT: " + str(listabancos) + "\n")
            return render_template("error_general.html", msg="Error obteniendo la lista de bancos, intente mas tarde",
                                   error="No es posible acceder a la lista de bancos emisores", type="500")
        else:
            logger.info(" TYPE: Lista bancos obtenida del archivo TXT: " + str(listabancos))



@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
@login_required
def pagomovil():
    form = FormFields()

    datos_cliente = session["datos_cliente"]
    montobs = session["monto_bs"]
    form.entity.choices = listabancos

    # Carga de los tipos de ID al selectfield ID
    form.tipo_id.choices = config.lista_id

    # Carga de los tipos de telefonos al selectfield PHONE
    form.tipo_phone.choices = config.lista_phone

    if form.validate_on_submit():  # Boton de aceptar

        id_customer = form.tipo_id.data + form.payerID.data
        phone_payer = form.tipo_phone.data[1:] + form.payerPhone.data
        entity = form.entity.data[:4]
        order = form.order.data
        montobs = session["monto_bs"]
        datos_cliente = session["datos_cliente"]
        img_entity = 'img/logo_bancoplaza.png'
        id_cliente = str(datos_cliente["datos"][0]["id"])
        client_id = str(datos_cliente["datos"][0]["cedula"])

        # VALIDO EL PAGO EN VIPPO
        logger.info("user: " + str(client_id) + " Validando el pago en vippo: " + id_customer +
                    "-" + phone_payer + "-" + entity + "-" + order + "-" + str(montobs))
        resultado_val = validar_pago(id_customer, phone_payer, entity, order, montobs)
        logger.debug("user: " + str(client_id) + " Resultado de validacion del pago: " + str(resultado_val))

        if resultado_val[0] == "success":
            if resultado_val[1]["message"] == "Operación realizada con éxito.":
                pago_validado = True
            else:
                img_result = 'img/error.png'
                return render_template('pay_result.html', msg=resultado_val[1]["result"]["label"],
                                       datos_cliente=datos_cliente, img_entity=img_entity,
                                       id_customer=id_customer,
                                       phone_payer=form.tipo_phone.data + form.payerPhone.data,
                                       entity=form.entity.data[6:], order=order, monto_bs=montobs,
                                       img_result=img_result)
        else:
            return render_template("error_general.html", msg="Error validando el pago, intente mas tarde",
                                   error=resultado_val[1], type="500")

        # BUSCO LAS FACTURAS EN MW SI SE VALIDA EL PAGO
        if pago_validado is True:
            monto_pagado = resultado_val[1]['result']['validatedPayments'][0]['amount']

            result_buscarfacturas = buscar_facturas(id_cliente, str(monto_pagado), montobs)
            logger.debug("user: " + str(client_id) +
                         " TYPE: Respuesta MW buscando facturas: " + str(result_buscarfacturas))

            if result_buscarfacturas[0] == "success":
                if result_buscarfacturas[1]["estado"] == "exito":
                    facturas_ubicadas = "True"
                else:
                    return render_template("error_general.html",
                                           msg="Error buscando facturas del cliente, intente mas tarde",
                                           error=str(resultado_val[1]), type="500")
            elif result_buscarfacturas[0] == "error":
                img_result = 'img/error.png'
                return render_template('pay_result.html', msg=result_buscarfacturas[1],
                                       datos_cliente=datos_cliente, img_entity=img_entity,
                                       id_customer=id_customer,
                                       phone_payer=form.tipo_phone.data + form.payerPhone.data,
                                       entity=form.entity.data[6:], order=order, monto_bs=montobs,
                                       img_result=img_result)
            else:
                return render_template("error_general.html",
                                       msg="Error buscando facturas del cliente, intente mas tarde",
                                       error=resultado_val[1], type="500")

            # PAGO LAS FACTURAS PENDIENTES
            if facturas_ubicadas:
                facturas = result_buscarfacturas[1]["facturas"]
                medio_pago = "pm_vippo"
                codigo_auth = form.order.data

                logger.debug("user: " + str(client_id) + " TYPE: pagando facturas: " + str(
                    facturas) + "-" + codigo_auth + "-" + medio_pago)

                pago_facturas = pagar_facturas(facturas, codigo_auth, medio_pago)

                logger.debug("user: " + str(
                    client_id) + " TYPE: Resultado del pago de facturas: " + str(pago_facturas))

                if pago_facturas[0] == "success":
                    if pago_facturas[1]["estado"] == "exito":
                        img_result = 'img/exito.png'
                        session.clear()
                        return render_template('pay_result.html', msg="Pago realizado con éxito",
                                               datos_cliente=datos_cliente, img_entity=img_entity,
                                               id_customer=id_customer,
                                               phone_payer=form.tipo_phone.data + form.payerPhone.data,
                                               entity=form.entity.data[6:], order=order, monto_bs=0,
                                               img_result=img_result)
                    else:
                        img_result = 'img/error.png'
                        return render_template('pay_result.html', msg="Error pagando factura",
                                               datos_cliente=datos_cliente, img_entity=img_entity,
                                               id_customer=id_customer,
                                               phone_payer=form.tipo_phone.data + form.payerPhone.data,
                                               entity=form.entity.data[6:], order=order, monto_bs=montobs,
                                               img_result=img_result)
                else:
                    return render_template("error_general.html", msg="Error pagando facturas, intente mas tarde",
                                           error=pago_facturas[1], type="500")

    else:
        return render_template('pagomovil.html', form=form, datos_cliente=datos_cliente,
                               pm_bancoplaza=config.pm_bancoplaza,
                               montobs=montobs)
