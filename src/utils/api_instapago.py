import requests
import os
import src.utils.connect_api as connect_api
from src.utils.logger import now, logger


def validar_pago(phonenumberclient, clientId, bank, reference, amount):
    today = now.strftime('%Y-%m-%d')
    endpoint = os.getenv("ENDPOINT_BASE_IP") + os.getenv("URL_VALIDATEPM_IP")
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
        "clientId": clientId,
        "bank": bank,
        "date": today,
        "reference": reference,
        "receiptbank": receiptbank,
        "amount": amount
    }

    api_response = connect_api.conectar(headers, body, params, endpoint, "GET", clientId)
    if api_response[0] == "success":
            return "success", api_response[1]
    elif api_response[0] == "except":
        return "except", api_response[1]
    else:
        return None