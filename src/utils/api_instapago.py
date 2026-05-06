import os
import src.utils.connect_api as connect_api
from flask_login import current_user


def validar_pago(phonenumberclient, id_pagador, bank, reference, amount, fecha_pago):
    date = fecha_pago.strftime('%Y-%m-%d')
    endpoint = os.getenv("ENDPOINT_BASE_IP") + os.getenv("URL_VALIDATEPM_IP")
    #endpoint = os.getenv("ENDPOINT_BASE_IP") + os.getenv("URL_CONSULTAPM_IP")
    keyId = os.getenv("KEYID_IP")
    publickeyid = os.getenv("PUBLICKEYID_IP")
    receiptbank = os.getenv("RECEIPTBANK_IP")


    # Creo el header y el body para validar el pago movil
    headers = {}
    # Body produccion
    body = {}
    params = {
        "keyId": keyId,
        "publickeyid": publickeyid,
        "phonenumberclient": phonenumberclient,
        "clientid": id_pagador,
        "bank": bank,
        "receiptbank": receiptbank,
        "date": date,
        "reference": reference,
        "amount": amount
    }

    api_response = connect_api.conectar(headers, body, params, endpoint, "GET", current_user.id)
    if api_response[0] == "success":
            return "success", api_response[1]
    elif api_response[0] == "except":
        return "except", api_response[1]
    else:
        return None

def orden_pago_tdc(amount, currency, order_number, concept):
    commerce_id = os.getenv("COMMERCE_ID")
    tipo_contenido = "application/json"

    base = os.getenv("ENDPOINT_BASE_IP_TDC", "")
    path = os.getenv("URL_TDC_IP", "")
    endpoint = f"{base}{path}"

    # Creo el header y el body para crear la orden de pago
    headers = {"CommerceId": commerce_id, "Content-Type": tipo_contenido}

    # Body produccion
    body = {"amount": amount,
            "Currency": currency,
            "OrderNumber": order_number,
            "Concept": concept
            }
    params = {}

    api_response = connect_api.conectar(headers, body, params, endpoint, "POST", current_user.id)
    if api_response[0] == "success":
        return "success", api_response[1]
    elif api_response[0] == "except":
        return "except", api_response[1]
    else:
        return None

def validar_pago_tdc(payment_request_id):
    commerce_id = os.getenv("COMMERCE_ID")
    tipo_contenido = "application/json"

    base = os.getenv("ENDPOINT_BASE_IP_TDC", "")
    path = os.getenv("URL_TDC_VALIDAR_PAGO", "")
    endpoint = f"{base}{path}"

    # Creo el header y el body para crear la orden de pago
    headers = {"CommerceId":commerce_id, "Content-Type": tipo_contenido}
    body = {}
    params = {"PaymentRequestId": payment_request_id}

    api_response = connect_api.conectar(headers, body, params, endpoint, "GET", current_user.id)
    if api_response[0] == "success":
            return "success", api_response[1]
    elif api_response[0] == "except":
        return "except", api_response[1]
    else:
        return None