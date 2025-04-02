
from flask import session, redirect, url_for, flash
from src.routes.home_bp.templates.form_fields import User
import os
import src.utils.connect_api as connect_api
from src.utils.logger import now, logger
from flask_login import current_user, login_user
import src.config as config
import math




today = now.strftime('%Y%m%d%H%M%S')


def buscar_cliente(client_id, client_email):
    headers = {"content-type": "application/json"}
    body = {"token": os.getenv("TOKEN_MW"), "cedula": client_id}
    endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_CLIENTE")

    api_response = connect_api.conectar(headers, body, endpoint,"POST", client_id)

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


def buscar_facturas(id_cliente, monto_pagado_bs, monto_deuda):
    monto_deuda_float = float(monto_deuda)
    # Valido la longitud del ID del cliente
    if len(id_cliente) < 1 or len(id_cliente) > 7:
        return "error", "idtraza muy largo"
        # Valido si el monto pagado es inferior a la deuda
    elif float(monto_pagado_bs) < int(monto_deuda_float):  # Omito los decimales de la deuda (solo entero)
        return "error", "Monto pagado (Bs." + monto_pagado_bs + ") esta por debajo de la deuda\
         (Bs." + str(monto_deuda) + ") debe contactarnos por WhatsApp al numero " + config.contacto_WhatsApp
    else:
        # Obtengo los codigos de las facturas pendientes por el cliente
        headers = {}
        body = {"token": os.getenv("TOKEN_MW"), "idcliente": id_cliente, "estado": "1"}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_FACTURAS")
        api_response = connect_api.conectar(headers, body, endpoint, "POST", current_user.id)
        return api_response

def pagar_facturas(facturas, codigo_auth, medio_pago, monto_pagado):
    cod_factura = 1
    headers = {"Content-Type": "application/json"}
    endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_PAGAR")
    monto_pagado_dls = float(monto_pagado) / float(session["tasa_bcv"])
    monto_pagado_dls = round(monto_pagado_dls, 2)  # trabajo con solo 2 decimales
    monto_pagado_dls_rounded = math.ceil(monto_pagado_dls)  # redondeo hacia arriba el monto pagado para evitar decimales

    if len(facturas) == 1:  # aplico solo cuando es una solo factura
        monto_factura = facturas[0]["total"]
        if monto_pagado_dls_rounded >= float(monto_factura):  # si el monto pagado es mayor o igual al total de la factura
            body = {"token": os.getenv("TOKEN_MW"),
                    "idfactura": facturas[0]["id"],
                    "pasarela": "API-" + medio_pago,
                    "cantidad": monto_pagado_dls,
                    "idtransaccion": codigo_auth + "-" + today + "-" + str(cod_factura)}
            api_response = connect_api.conectar(headers, body, endpoint, "POST", current_user.id)
        else:
            return "error", "Monto pagado (Bs." + monto_pagado + ") esta por debajo de la deuda\
         (Bs." + str(facturas[0]["total"]) + ") debe contactarnos por WhatsApp al numero " + config.contacto_WhatsApp

    elif len(facturas) > 1:
        for factura in facturas:
            monto_factura = factura["total"]

            if monto_pagado_dls_rounded >= float(monto_factura):  # si el monto pagado es mayor o igual al total de la factura
                body = {"token": os.getenv("TOKEN_MW"),
                        "idfactura": facturas[0]["id"],
                        "pasarela": "API-" + medio_pago,
                        "cantidad": monto_factura,
                        "idtransaccion": codigo_auth + "-" + today + "-" + str(cod_factura)}
                api_response = connect_api.conectar(headers, body, endpoint, "POST", current_user.id)
                cod_factura = cod_factura + 1
            else:
                return "error", "Monto pagado (Bs." + monto_pagado + ") esta por debajo de la deuda\
             (Bs." + str(
                    facturas[0]["total"]) + ") debe contactarnos por WhatsApp al numero " + config.contacto_WhatsApp





        return api_response

