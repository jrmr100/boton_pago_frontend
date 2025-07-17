from flask import render_template, Blueprint, session
from src.routes.tarjetas_credito_bp.templates.form_fields_tc import FormFieldsTc
from src.utils.api_mw import buscar_facturas, pagar_facturas
from src.utils.api_instapago import InstaPago
from flask_login import login_required, current_user
import src.config as config

nombre_ruta = "tarjetas_credito"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
@login_required
def tarjetas_credito():
    form_tc = FormFieldsTc()
    datos_cliente = current_user.datos_cliente
    montobs = session["monto_bs"]

    # Carga de los tipos de ID al selectfield ID
    form_tc.tipo_id.choices = config.lista_id

    ################## SUBMIT ##################
    if form_tc.validate_on_submit():
        id_pagador = form_tc.tipo_id.data + form_tc.ci.data
        montobs = f"{form_tc.monto.data:.2f}"
        descripcion = form_tc.descripcion.data
        nombre = form_tc.nombre.data
        numero_tc = form_tc.numero_tc.data
        codigo_seguridad = form_tc.codigo_seguridad.data
        fecha_vencimiento = form_tc.fecha_vencimiento.data

        # VALIDO EL PAGO EN INSTAPAGO
        validar_pago = InstaPago()
        resultado_val = validar_pago.validar_pm(id_pagador, montobs, descripcion, nombre, numero_tc, codigo_seguridad)

        img_entity = config.pm_bancoplaza["logo"]
        id_cliente = str(datos_cliente["id"])

        if resultado_val[0] == "success":
            if resultado_val[1]["message"] == "Operación realizada con éxito.":
                pago_validado = True
            else:
                img_result = 'img/error.png'
                return render_template('pagomovil_result.html', msg=resultado_val[1]["result"]["label"],
                                       img_entity=img_entity,
                                       id_customer=id_pagador,
                                       phone_payer=form_tc.tipo_phone.data + form_tc.payerPhone.data,
                                       entity=form_tc.entity.data[6:], order=order, monto_bs=montobs,
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
                                       img_entity=img_entity,
                                       id_customer=id_pagador,
                                       phone_payer=form_tc.tipo_phone.data + form_tc.payerPhone.data,
                                       entity=form_tc.entity.data[6:], order=order, monto_bs=montobs,
                                       img_result=img_result, datos_cliente=datos_cliente)
            else:
                return render_template("error_general.html",
                                       msg="Error buscando facturas del cliente, intente mas tarde",
                                       error=resultado_val[1], type="500")

            # PAGO LAS FACTURAS PENDIENTES
            if facturas_ubicadas:
                facturas = result_buscarfacturas[1]["facturas"]
                medio_pago = "pm_vippo"
                codigo_auth = form_tc.order.data

                pago_facturas = pagar_facturas(facturas, codigo_auth, medio_pago, monto_pagado)

                if pago_facturas[0] == "success":
                    if pago_facturas[1]["estado"] == "exito":
                        img_result = 'img/exito.png'
                        return render_template('pagomovil_result.html', msg="Pago realizado con éxito",
                                               img_entity=img_entity,
                                               id_customer=id_pagador,
                                               phone_payer=form_tc.tipo_phone.data + form_tc.payerPhone.data,
                                               entity=form_tc.entity.data[6:], order=order, monto_bs=0,
                                               img_result=img_result, datos_cliente=datos_cliente)
                    else:
                        img_result = 'img/error.png'
                        return render_template('pagomovil_result.html', msg="Error pagando factura",
                                               img_entity=img_entity,
                                               id_customer=id_pagador,
                                               phone_payer=form_tc.tipo_phone.data + form_tc.payerPhone.data,
                                               entity=form_tc.entity.data[6:], order=order, monto_bs=montobs,
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
        return render_template('tarjetas_credito.html', form=form_tc, datos_cliente=datos_cliente,
                               tarjetas_credito=config.tarjetas_credito, pm_bancoplaza=config.pm_bancoplaza, montobs=montobs)

