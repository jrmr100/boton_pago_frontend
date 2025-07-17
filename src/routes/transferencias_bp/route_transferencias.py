from flask import render_template, Blueprint, session
from src.routes.transferencias_bp.templates.form_fields_transferencias import FormFieldsTransferencias
from src.utils.api_mw import buscar_facturas, pagar_facturas
from src.utils.api_vippo import leer_listabancos
from src.utils.api_instapago import InstaPago
from flask_login import login_required, current_user
import src.config as config

nombre_ruta = "transferencias"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)

# Cargo la lista de bancos solo una vez cuando se acceda a la ruta transferencias
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


@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
@login_required
def transferencias():
    form_transferencias = FormFieldsTransferencias()
    datos_cliente = current_user.datos_cliente
    montobs = session["monto_bs"]
    form_transferencias.banco_emisor.choices = listabancos

    # Carga de los tipos de ID al selectfield ID
    form_transferencias.tipo_id.choices = config.lista_id


    ################## SUBMIT ##################
    if form_transferencias.validate_on_submit():
        id_pagador = form_transferencias.tipo_id.data + form_transferencias.ci.data
        fecha_pago = form_transferencias.fecha_pago.data
        banco_emisor = form_transferencias.banco_emisor.data
        montobs = f"{form_transferencias.monto.data:.2f}"
        montobs="10.00"
        referencia = form_transferencias.referencia.data
        datos_cliente = current_user.datos_cliente
        logo = config.pm_bancoplaza["logo"]
        id_cliente = str(datos_cliente["id"])
        client_id = str(datos_cliente["cedula"])

        # VALIDO EL PAGO EN INSTAPAGO
        validar_pago = InstaPago()
        resultado_val = validar_pago.validar_transfer(fecha_pago, referencia, id_pagador, banco_emisor[:4], montobs)

        if resultado_val[0] == "success":
            if resultado_val[1]["message"] == "Operación realizada con éxito.":
                pago_validado = True
            else:
                img_result = 'img/error.png'
                return render_template('transferencias.html', msg=resultado_val[1]["result"]["label"],
                                       logo=logo,
                                       id_pagador=id_pagador,
                                       banco_emisor=form_transferencias.banco_emisor.data[6:], referencia=referencia, monto_bs=montobs,
                                       img_result=img_result, datos_cliente=datos_cliente)
        else:
            return render_template("error_general.html", msg="Error validando el pago, intente mas tarde",
                                   error=resultado_val[1], type="500")

        # BUSCO LAS FACTURAS EN MW SI SE VALIDA EL PAGO
        if pago_validado is True:
            monto_pagado = resultado_val[1]['result']['validatedPayments'][0]['amount']

            result_buscarfacturas = buscar_facturas(id_cliente, monto_pagado)

            if result_buscarfacturas[0] == "success":
                if result_buscarfacturas[1]["estado"] == "exito":
                    facturas_ubicadas = "True"
                else:
                    return render_template("error_general.html",
                                           msg="Error buscando facturas del cliente, intente mas tarde",
                                           error=str(resultado_val[1]), type="500")
            elif result_buscarfacturas[0] == "error":
                img_result = 'img/error.png'
                return render_template('pagomovil_result.html', msg=result_buscarfacturas[1],
                                       img_entity=logo,
                                       id_customer=id_pagador,
                                       phone_payer=form_transferencias.tipo_phone.data + form_transferencias.payerPhone.data,
                                       entity=form_transferencias.entity.data[6:], order=order, monto_bs=montobs,
                                       img_result=img_result, datos_cliente=datos_cliente)
            else:
                return render_template("error_general.html",
                                       msg="Error buscando facturas del cliente, intente mas tarde",
                                       error=resultado_val[1], type="500")

            # PAGO LAS FACTURAS PENDIENTES
            if facturas_ubicadas:
                facturas = result_buscarfacturas[1]["facturas"]
                medio_pago = "pm_vippo"
                codigo_auth = form_transferencias.order.data

                pago_facturas = pagar_facturas(facturas, codigo_auth, medio_pago, monto_pagado)

                if pago_facturas[0] == "success":
                    if pago_facturas[1]["estado"] == "exito":
                        img_result = 'img/exito.png'
                        return render_template('pagomovil_result.html', msg="Pago realizado con éxito",
                                               img_entity=logo,
                                               id_customer=id_pagador,
                                               phone_payer=form_transferencias.tipo_phone.data + form_transferencias.payerPhone.data,
                                               entity=form_transferencias.entity.data[6:], order=referencia, monto_bs=0,
                                               img_result=img_result, datos_cliente=datos_cliente)
                    else:
                        img_result = 'img/error.png'
                        return render_template('pagomovil_result.html', msg="Error pagando factura",
                                               img_entity=logo,
                                               id_customer=id_pagador,
                                               phone_payer=form_transferencias.tipo_phone.data + form_transferencias.payerPhone.data,
                                               entity=form_transferencias.entity.data[6:], order=referencia, monto_bs=montobs,
                                               img_result=img_result, datos_cliente=datos_cliente)
                else:
                    return render_template("error_general.html", msg="Error pagando facturas, intente mas tarde",
                                           error=pago_facturas[1], type="500")
            else:
                return render_template("error_general.html", msg="Error pagando facturas, intente mas tarde",
                                       error="Facturas ubicadas is not true", type="500")
        else:
            return render_template("error_general.html", msg="Error validando pago, intente mas tarde",
                                   error="Facturas ubicadas is not true", type="500")

    else:
        return render_template('transferencias.html', form=form_transferencias, datos_cliente=datos_cliente,
                               transferencias=config.transferencias, pm_bancoplaza=config.pm_bancoplaza, montobs=montobs)

