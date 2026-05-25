from flask import render_template, Blueprint, session, redirect, url_for, flash, request
from src.routes.pagos_bp.templates.form_fields import FormFields
from flask_login import login_required, current_user
from src.utils.logger import logger
from src.utils.api_instapago import validar_pago_tdc
from src.utils.api_mw import buscar_facturas, pagar_facturas
from src.utils.database import actualizar_pago_db

nombre_ruta = "resultado_pagos"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


@blue_ruta.route('/' + nombre_ruta, methods=["GET"])
@login_required
def resultado_pagos():
    # PASO 3 - Retorno al comercio
    form = FormFields()
    datos_cliente = current_user.datos_cliente

    # Capturar el payment_request_id que envía el portal de instapago
    payment_request_id = request.args.get('PaymentRequestId')
    if not payment_request_id:
        logger.warning(f"USER:{current_user.id}: Intento de acceso a resultado_pagos sin PaymentRequestId.")
        return redirect(url_for('pagos.pagos'))
    logger.info(f"USER:{current_user.id}: Se recibio payment_request_id: {payment_request_id}")

    # PASO 4 - Consultat el estado del pago
    api_response = validar_pago_tdc(payment_request_id)

    status_final = "REJECTED"
    detalles = {}

    if api_response[0] == "success":
        data = api_response[1].get("data", {})
        payment_processed = data.get("paymentProcessed")
        request_info = data.get("paymentRequest")

        # Regla clave del manual: Si hay paymentProcessed, usar ese. Si no, usar paymentRequest.
        if payment_processed:
            status_final = payment_processed.get("processedStatus")  # APPROVED o REJECTED
            detalles = payment_processed
        else:
            status_final = request_info.get("requestStatus")  # INPROCESS o REJECTED
            detalles = request_info

    # 3. Actualizar tu base de datos local (Persistencia)
    from src.utils.database import actualizar_pago_db
    actualizar_pago_db(payment_request_id, status_final)

    status_final = "APPROVED"
    # 4. Lógica de respuesta al usuario
    if status_final == "APPROVED":
        logger.info(f"USER:{current_user.id}: Pago {payment_request_id} en estado APPROVED")

        # BUSCO LAS FACTURAS EN MW SI SE APRUEBA EL PAGO
        monto_pagado = detalles.get("amount")
        result_buscarfacturas = buscar_facturas(datos_cliente["id"], monto_pagado)

        if result_buscarfacturas[0] == "success":
            if result_buscarfacturas[1]["estado"] == "exito":
                facturas_ubicadas = "True"
                logger.info(f"USER:{current_user.id}: Facturas {datos_cliente['id']} ubicadas exitosamente")
            else:
                logger.error(f"USER:{current_user.id}: Error buscando facturas del cliente: {result_buscarfacturas[1]}")
                return render_template("error_general.html",
                                       msg="Error buscando facturas del cliente, intente mas tarde",
                                       error=str(result_buscarfacturas[1]), type="500")
        elif result_buscarfacturas[0] == "error":
            logger.error(f"USER:{current_user.id}: Error buscando facturas del cliente: {result_buscarfacturas[1]}")
            img_result = 'img/error.png'
            img_entity = 'img/credit-card.png'
            order = session["order_number"]
            return render_template('resultado_pago.html', msg="ESTADO DEL PAGO: ERROR",
                                   img_entity=img_entity, order=order, monto_bs=datos_cliente["total_facturas"],
                                   img_result=img_result, datos_cliente=datos_cliente, medio_pago="TDC")

        else:
            logger.error(f"USER:{current_user.id}: Error buscando facturas del cliente: {result_buscarfacturas[1]}")
            return render_template("error_general.html",
                                   msg="Error buscando facturas del cliente, intente mas tarde",
                                   error=result_buscarfacturas[1], type="500")
        # PAGO LAS FACTURAS PENDIENTES
        if facturas_ubicadas:
            logger.info(f"USER:{current_user.id}: Facturas {datos_cliente['id']} ubicadas exitosamente")
            facturas = result_buscarfacturas[1]["facturas"]
            medio_pago = "tdc_instapago"
            codigo_auth = detalles.get("approvalNumber")

            pago_facturas = pagar_facturas(facturas, codigo_auth, medio_pago, monto_pagado)

            if pago_facturas[0] == "success":
                if pago_facturas[1]["estado"] == "exito":
                    logger.info(f"USER:{current_user.id}: Facturas {datos_cliente['id']} pagadas exitosamente")
                    img_result = 'img/exito.png'
                    img_entity = 'img/credit-card.png'
                    order = session["order_number"]
                    return render_template('resultado_pago.html', msg="ESTADO DEL PAGO: EXITOSO",
                                           img_entity=img_entity, order=order, monto_bs=datos_cliente["total_facturas"],
                                           img_result=img_result, datos_cliente=datos_cliente, medio_pago="TDC")
                else:
                    logger.error(f"USER:{current_user.id}: Error pagando facturas: {pago_facturas[1]}")
                    img_result = 'img/error.png'
                    return render_template("error_general.html",
                                           msg="Error buscando facturas del cliente, intente mas tarde",
                                           error=str(result_buscarfacturas[1]), type="500")
            else:
                logger.error(f"USER:{current_user.id}: Error pagando facturas: {pago_facturas[1]}")
                return render_template("error_general.html", msg="Error pagando facturas, intente mas tarde",
                                       error=pago_facturas[1], type="500")
        else:
            logger.error(f"USER:{current_user.id}: Error pagando facturas: Facturas ubicadas is not true")
            return render_template("error_general.html", msg="Error pagando facturas, intente mas tarde",
                                   error="Facturas ubicadas is not true", type="500")

    elif status_final == "INPROCESS":
        logger.info(f"USER:{current_user.id}: Pago {payment_request_id} en estado INPROCESS")
        img_result = 'img/informacion.jpg'
        img_entity = 'img/credit-card.png'
        order = session["order_number"]
        return render_template('resultado_pago.html', msg="ESTADO DEL PAGO: EN PROCESO",
                               img_entity=img_entity, order=order, monto_bs=datos_cliente["total_facturas"],
                               img_result=img_result, datos_cliente=datos_cliente, medio_pago="TDC")

    else:
        logger.info(f"USER:{current_user.id}: Pago {payment_request_id} en estado RECHAZADO")
        img_result = 'img/error.png'
        img_entity = 'img/credit-card.png'
        order = session["order_number"]
        actualizar_pago = actualizar_pago_db(payment_request_id, status_final)
        if actualizar_pago is True:
            logger.error(
                f"USER:{current_user.id}: Pago actualizado en BD: {payment_request_id} con status {status_final}")
            return render_template('resultado_pago.html', msg="ESTADO DEL PAGO: RECHAZADO",
                                   img_entity=img_entity, order=order, monto_bs=datos_cliente["total_facturas"],
                                   img_result=img_result, datos_cliente=datos_cliente, medio_pago="TDC")
        else:
            logger.error(
                f"USER:{current_user.id}: Error al actualizar el pago en BD {payment_request_id} con status {status_final}")
            return render_template('resultado_pago.html', msg="ESTADO DEL PAGO: RECHAZADO",
                                   img_entity=img_entity, order=order, monto_bs=datos_cliente["total_facturas"],
                                   img_result=img_result, datos_cliente=datos_cliente, medio_pago="TDC")
