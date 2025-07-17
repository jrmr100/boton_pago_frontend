from flask_login import current_user
import src.utils.connect_api as connect_api
import os


class InstaPago:
    def __init__(self):
        self.keyId = os.getenv("KEYID_IP")
        self.publickeyid = os.getenv("PUBLICKEYID_IP")

    def validar_pm(self, phonenumberclient, id_pagador, bank, reference, amount, fecha_pago):
        date = fecha_pago.strftime('%Y-%m-%d')
        endpoint = os.getenv("ENDPOINT_BASE_IP") + os.getenv("URL_VALIDATEPM_IP")
        keyid = self.keyId
        publickeyid = self.publickeyid
        receiptbank = os.getenv("RECEIPTBANK_IP")

        # Creo el header y el body para validar el pago movil
        headers = {}
        # Body produccion
        body = {}
        params = {
            "keyId": keyid,
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
        if api_response[0]:
            return "success", api_response[1]
        elif api_response[0] == "except":
            return "except", api_response[1]
        else:
            return None

    def validar_transfer(self, fecha, referencia, id_cliente, banco_emisor, monto):
        keyid = self.keyId
        publickeyid = self.publickeyid
        fecha = fecha.strftime('%Y-%m-%d')
        referencia = referencia
        id_cliente = id_cliente
        banco_receptor = os.getenv("RECEIPTBANK_IP")
        banco_emisor = banco_emisor
        monto = monto
        endpoint = os.getenv("ENDPOINT_BASE_IP") + os.getenv("URL_VALIDATETRANF_IP")

        # Creo el header y el body para validar la transferecnia
        headers = {}
        # Body produccion
        body = {"keyId": keyid,
                "publickeyid": publickeyid,
                "date": fecha,
                "reference": referencia,
                "clientid": id_cliente,
                "receiptbank": banco_receptor,
                "bank": banco_emisor,
                "amount": monto
                }
        params = {}
        api_response = connect_api.conectar(headers, body, params, endpoint, "GET", current_user.id)
        if api_response[0]:
            return "success", api_response[1]
        elif api_response[0] == "except":
            return "except", api_response[1]
        else:
            return None
