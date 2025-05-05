from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.pagomovil_bp.templates.form_fields_reportes import FormFieldsReportes
from src.utils.api_instapago import validar_pago
from src.utils.api_vippo import leer_listabancos
from src.utils.logger import logger
from flask_login import login_required, current_user
import src.config as config
from src.utils.api_mw import buscar_facturas, pagar_facturas


nombre_ruta = "pagomovil_banesco"

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
@login_required
def cargar_listabancos():
    global listabancos
    if listabancos is None:
        listabancos = leer_listabancos()
        # Carga de los bancos emisores al selectfield ENTITY
        if "error listabancos" in listabancos:
            return render_template("error_general.html", msg="Error obteniendo la lista de bancos, intente mas tarde",
                                   error="No es posible acceder a la lista de bancos emisores", type="500")


@blue_ruta.after_request
def add_header(response):
    """
    Evito que los navegadores metan en cache
    esta pagina y no afecte el spinner
    """
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response



@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
@login_required
def pagomovil_banesco():
    form_reportes = FormFieldsReportes()
    datos_cliente = current_user.datos_cliente
    montobs = session["monto_bs"]
    form_reportes.entity.choices = listabancos

    # Carga de los tipos de ID al selectfield ID
    form_reportes.tipo_id.choices = config.lista_id

    # Carga de los tipos de telefonos al selectfield PHONE
    form_reportes.tipo_phone.choices = config.lista_phone

    if form_reportes.validate_on_submit():
        id_customer = form_reportes.tipo_id.data + form_reportes.payerID.data
        phonenumberclient = "0058" + form_reportes.tipo_phone.data[1:] + form_reportes.payerPhone.data
        bank = form_reportes.entity.data[:4]
        reference = form_reportes.order.data
        # amount = session["monto_bs"]
        amount = form_reportes.monto.data
        datos_cliente = current_user.datos_cliente
        img_entity = config.pm_banesco[3]
        id_cliente = str(datos_cliente["id"])
        clientId = str(form_reportes.tipo_id.data) + str(form_reportes.payerID.data)
        pago_validado = False

        # VALIDO EL PAGO EN INSTAPAGO
        resultado_val = validar_pago(phonenumberclient, clientId, bank, reference, amount)

        if resultado_val[0] == "success":
            if resultado_val[1]["message"] == "Se ha encontrado un pago, exitosamente":
                pago_validado = True
            else:
                img_result = 'img/error.png'
                return render_template('pagomovil_result.html', msg=resultado_val[1]["message"],
                                       img_entity=img_entity,
                                       id_customer=id_customer,
                                       phone_payer=form_reportes.tipo_phone.data + form_reportes.payerPhone.data,
                                       entity=form_reportes.entity.data[6:], order=reference, monto_bs=montobs,
                                       img_result=img_result, datos_cliente=datos_cliente)

        else:
            return render_template("error_general.html", msg="Error validando el pago, intente mas tarde",
                                   error=resultado_val[1], type="500")

        # BUSCO LAS FACTURAS EN MW SI SE VALIDA EL PAGO
        if pago_validado is True:
            monto_pagado = resultado_val[1]['amount']

            result_buscarfacturas = buscar_facturas(id_cliente, str(monto_pagado), montobs)
            logger.debug("USER: " + str(id_customer) +
                         " TYPE: Respuesta MW buscando facturas: " + str(result_buscarfacturas))

            if result_buscarfacturas[0] == "success":
                if result_buscarfacturas[1]["estado"] == "exito":
                    facturas_ubicadas = "True"
                else:
                    return render_template("error_general.html",
                                           msg="Error buscando facturas del cliente, intente mas tarde",
                                           error=str(result_buscarfacturas[1]), type="500")
            elif result_buscarfacturas[0] == "error":
                img_result = 'img/error.png'
                return render_template('pagomovil_result.html', msg=result_buscarfacturas[1],
                                       img_entity=img_entity,
                                       id_customer=id_customer,
                                       phone_payer=form_reportes.tipo_phone.data + form_reportes.payerPhone.data,
                                       entity=form_reportes.entity.data[6:], order=reference, monto_bs=montobs,
                                       img_result=img_result, datos_cliente=datos_cliente)
            else:
                return render_template("error_general.html",
                                       msg="Error buscando facturas del cliente, intente mas tarde",
                                       error=result_buscarfacturas[1], type="500")
            # PAGO LAS FACTURAS PENDIENTES
            if facturas_ubicadas:
                facturas = result_buscarfacturas[1]["facturas"]
                medio_pago = "pm_instapago"
                codigo_auth = form_reportes.order.data

                logger.debug("USER: " + str(clientId) + " TYPE: pagando facturas: " + str(
                    facturas) + "-" + codigo_auth + "-" + medio_pago)

                pago_facturas = pagar_facturas(facturas, codigo_auth, medio_pago)

                if pago_facturas[0] == "success":
                    if pago_facturas[1]["estado"] == "exito":
                        img_result = 'img/exito.png'
                        return render_template('pagomovil_result.html', msg="Pago realizado con éxito",
                                               img_entity=img_entity,
                                               id_customer=id_customer,
                                               phone_payer=form_reportes.tipo_phone.data + form_reportes.payerPhone.data,
                                               entity=form_reportes.entity.data[6:], order=reference, monto_bs=0,
                                               img_result=img_result, datos_cliente=datos_cliente)
                    else:
                        img_result = 'img/error.png'
                        return render_template('pagomovil_result.html', msg="Error pagando factura",
                                               img_entity=img_entity,
                                               id_customer=id_customer,
                                               phone_payer=form_reportes.tipo_phone.data + form_reportes.payerPhone.data,
                                               entity=form_reportes.entity.data[6:], order=reference, monto_bs=montobs,
                                               img_result=img_result, datos_cliente=datos_cliente)
                else:
                    return render_template("error_general.html", msg="Error pagando facturas, intente mas tarde",
                                           error=pago_facturas[1], type="500")
            else:
                return render_template("error_general.html", msg="Error pagando facturas, intente mas tarde",
                                       error="Facturas ubicadas is not true", type="500")
        else:
            return render_template("error_general.html",
                                       msg="Error buscando facturas del cliente, intente mas tarde",
                                       error="Error validando el pago", type="500")

    else:
        return render_template('pagomovil_reportes.html', form=form_reportes, datos_cliente=datos_cliente,
                           pm_pagomovil=config.pm_banesco, montobs=montobs)
