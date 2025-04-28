
from flask import render_template, Blueprint, session, redirect, url_for, flash
from src.routes.home_bp.templates.form_fields import User
import os
import src.utils.connect_api as connect_api
from src.utils.logger import now, logger
from flask_login import current_user, login_user
import src.config as config



today = now.strftime('%Y%m%d%H%M%S')


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


def buscar_facturas(id_cliente, monto_pagado_bs, monto_deuda):

    # Valido la longitud del ID del cliente
    if len(id_cliente) < 1 or len(id_cliente) > 7:
        return "error", "idtraza muy largo"

        # Valido si el monto pagado es inferior a la deuda
    elif float(monto_pagado_bs) < float(monto_deuda):
        return "error", "Monto pagado (Bs." + monto_pagado_bs + ") esta por debajo de la deuda\
         (Bs." + str(monto_deuda) + ") debe contactarnos por WhatsApp al numero " + config.contacto_WhatsApp
    else:
        # Obtengo los codigos de las facturas pendientes por el cliente
        headers = {}
        params = {}
        body = {"token": os.getenv("TOKEN_MW"), "idcliente": id_cliente, "estado": "1"}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_FACTURAS")
        api_response = connect_api.conectar(headers, body, params, endpoint, "POST", current_user.id)
        return api_response

def pagar_facturas(facturas, codigo_auth, medio_pago):
    cod_factura = 1
    params = {}
    headers = {"Content-Type": "application/json"}
    endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_PAGAR")

    for factura in facturas:
        body = {"token": os.getenv("TOKEN_MW"),
                   "idfactura": factura["id"],
                   "pasarela": "API-" + medio_pago,
                   "idtransaccion": codigo_auth + "-" + today + "-" + str(cod_factura)}
        api_response = connect_api.conectar(headers, body, params, endpoint, "POST", current_user.id)
        cod_factura = cod_factura + 1

    return api_response

