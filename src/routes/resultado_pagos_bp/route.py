from flask import render_template, Blueprint, session, redirect, url_for, flash, request
from src.routes.pagos_bp.templates.form_fields import FormFields
from flask_login import login_required, current_user
from src.utils.logger import logger
from src.utils.api_instapago import validar_pago_tdc

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
    form = FormFields()
    datos_cliente = current_user.datos_cliente

    # 1. Capturar el payment_request_id que envía el portal de instapago
    payment_request_id = request.args.get('PaymentRequestId')
    if not payment_request_id:
        logger.warning(f"USER:{current_user.id}: Intento de acceso a resultado_pagos sin ID.")
        return redirect(url_for('pagos.pagos'))
    logger.info(f"USER:{current_user.id}: Se recibio payment_request_id: {payment_request_id}")

    # 2. Consultar la API de instapago para validar el resultado del pago
    api_response = validar_pago_tdc(payment_request_id)

    status_final = "REJECTED"
    detalles = {}

    if api_response[0] == "success":
        data = api_response[1].get("data", {})
        processed = data.get("paymentProcessed")
        request_info = data.get("paymentRequest")

        # Regla clave del manual: Si hay paymentProcessed, usar ese. Si no, usar paymentRequest.
        if processed:
            status_final = processed.get("processedStatus")  # APPROVED o REJECTED
            detalles = processed
        elif request_info:
            status_final = request_info.get("requestStatus")  # INPROCESS o REJECTED
            detalles = request_info

    """# 3. Actualizar tu base de datos local (Persistencia)
    from src.utils.database import actualizar_pago_db
    actualizar_pago_db(payment_request_id, status_final)

    # 4. Lógica de respuesta al usuario
    if status_final == "APPROVED":
        flash("¡Pago procesado exitosamente!", "success")
        # Aquí podrías disparar lógica adicional: enviar correo, activar servicio, etc.
    elif status_final == "INPROCESS":
        flash("El pago aún está en proceso o fue abandonado.", "info")
    else:
        flash("El pago fue rechazado o falló. Intente nuevamente.", "failure")"""

    return render_template("resultado_pagos.html", datos_cliente=datos_cliente,
                           paymentid=payment_request_id, form=form)
