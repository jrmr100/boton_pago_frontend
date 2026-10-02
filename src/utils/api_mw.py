
from flask import session
from src.routes.home_bp.templates.form_fields import User
import os
import src.utils.connect_api as connect_api
from src.utils.logger import logger
from flask_login import current_user, login_user
import src.config as config
from datetime import datetime


def buscar_cliente(client_id, client_email):
    headers = {"content-type": "application/json"}
    body = {"token": os.getenv("TOKEN_MW"), "cedula": client_id}
    endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_CLIENTE")
    params = {}

    api_response = connect_api.conectar(headers, body, params, endpoint,"POST", client_id)

    if api_response[0] == "success":
        if api_response[1]["estado"] == "exito":  # Cliente obtenido
            ###### VALIDO EL CORREO DEL CLIENTE ######
            email_mw = api_response[1]['datos'][0]['correo']
            if client_email.lower() == email_mw.lower():
                # Almaceno la session
                session.permanent = True  # Permite utilizar el tiempo de vida de la session
                datos_cliente = {"nombre": api_response[1]["datos"][0]["nombre"],
                                 "id": api_response[1]["datos"][0]["id"],
                                 "cedula": api_response[1]["datos"][0]["cedula"],
                                 "estado": api_response[1]["datos"][0]["estado"],
                                 "movil": api_response[1]["datos"][0]["movil"],
                                 "facturas_nopagadas": api_response[1]["datos"][0]["facturacion"][
                                     "facturas_nopagadas"],
                                 "total_facturas": api_response[1]["datos"][0]["facturacion"]["total_facturas"]
                                 }
                session["datos_cliente"] = datos_cliente
                user = User(client_id, datos_cliente)
                login_user(user)
                return api_response

            else:
                logger.error("USER: " + str(client_id) + " TYPE: No coinciden los correos " + "\n")
                return "error", "No existe el cliente con el filtro indicado."
        elif api_response[1]["estado"] == "error":
            # log se muestra desde respuesta de la api
            return "error", api_response[1]["mensaje"]
    else:
        return "except", api_response[1]


def buscar_facturas(id_cliente, monto_pagado):
    monto_deuda = float(session["monto_bs"])
    porcentaje_deuda = os.getenv("PORCENTAJE_DEUDA_MINIMA")
    if float(porcentaje_deuda) > 0 and float(porcentaje_deuda) < 100:
        factor_pago = round(1 - (float(porcentaje_deuda) / 100), 2)
        deuda_minima = round(float(monto_deuda) * factor_pago, 2)  # Deuda con el porcentaje tolerable por debajo
    else:
        deuda_minima = monto_deuda
    session["deuda_minima"] = deuda_minima

    # Registro el log de la aprobacion del pago por debajo de la deuda
    if float(monto_pagado) < monto_deuda and float(monto_pagado) >= deuda_minima:
        logger.warning(f"USER: {str(id_cliente)} TYPE: Pago realizado ({monto_pagado}) esta por debajo de la deuda ({monto_deuda})\n")

    # Valido la longitud del ID del cliente
    if len(id_cliente) < 1 or len(id_cliente) > 7:
        logger.error("USER: " + str(id_cliente) + " TYPE: idcliente no valido" + "\n")
        return "error", "id-cliente no valido"

    # Valido si el monto pagado es inferior a la deuda minima
    elif float(monto_pagado) < float(deuda_minima):
        msg = (f"Monto pagado (Bs.{monto_pagado}) esta por debajo de la deuda (Bs.{monto_deuda})"
               f" debe contactarnos por WhatsApp al numero {config.contacto_WhatsApp}")
        logger.error(f"USER: {str(id_cliente)} - TYPE: {msg}")
        return "error", msg
    else:
        # Obtengo los codigos de las facturas pendientes por el cliente
        headers = {}
        params = {}
        body = {"token": os.getenv("TOKEN_MW"), "idcliente": id_cliente, "estado": "1"}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_FACTURAS")
        api_response = connect_api.conectar(headers, body, params, endpoint, "POST", current_user.id)
        return api_response

def pagar_facturas(facturas, codigo_auth, medio_pago, monto_pagado):
    cod_factura = 1
    params = {}
    headers = {"Content-Type": "application/json"}
    endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_PAGAR")
    monto_deuda = float(session["monto_bs"])
    deuda_minima = float(session["deuda_minima"]) #obtenida en buscar_facturas
    pago = float(monto_pagado)
    today = datetime.now().strftime('%Y%m%d%H%M%S')  # Fecha del pago, no del arranque del proceso

    # Sin facturas pendientes el pago validado no se puede aplicar, debe revisarse manualmente
    if not facturas:
        msg = f"No hay facturas pendientes para aplicar el pago {codigo_auth} (Bs.{monto_pagado})"
        logger.error(f"USER: {current_user.id} - TYPE: {msg}\n")
        return "error", msg

    diff_pago = pago - monto_deuda  # Para validar si el pago es exacto

    pago_aceptado = False
    if pago >= deuda_minima and pago < monto_deuda:
        pago_aceptado = True
    elif diff_pago == 0:
        pago_aceptado = True

    if not pago_aceptado:  # Indica que el pago esta por encima de la deuda (si esta por debajo lo valida buscar_facturas)
        diff_pago_dls = diff_pago / float(session["tasa_bcv"])
    ultima_factura = len(facturas) - 1

    primer_fallo = None
    for i in range(len(facturas)):   # Reviso todas las facturas
        body = {"token": os.getenv("TOKEN_MW"),
                "idfactura": facturas[i]["id"],
                "pasarela": "API-" + medio_pago,
                "idtransaccion": codigo_auth + "-" + today + "-" + str(cod_factura)}
        if not pago_aceptado and i == ultima_factura:   # Solo a la ultima factura le sumo la diferencia
            cantidad = float(facturas[i]["total"]) + diff_pago_dls
            body["cantidad"] = float(f"{cantidad:.2f}")
        # Si no agrego cantidad se paga completa la factura

        api_response = connect_api.conectar(headers, body, params, endpoint, "POST", current_user.id)
        cod_factura = cod_factura + 1

        # Continuo con las demas facturas pero recuerdo el primer fallo para no reportar exito
        if api_response[0] != "success" or api_response[1].get("estado") != "exito":
            logger.error(f"USER: {current_user.id} - TYPE: Error pagando factura {facturas[i]['id']}"
                         f" del pago {codigo_auth}: {api_response[1]}\n")
            if primer_fallo is None:
                primer_fallo = api_response

    if primer_fallo is not None:
        return primer_fallo
    return api_response

