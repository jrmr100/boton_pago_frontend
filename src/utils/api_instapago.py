import requests
import os
import src.utils.connect_api as connect_api
from src.utils.logger import now, logger



def generar_qr():
    url = "https://merchant.instapago.com/services/api/v2/Payments/GetPaymentAffiliateQR?PublicKeyId=e46dc9c8ce04bccfd742322b3ccc9049&KeyId=890AB86E-5938-4CEB-BC37-CA8C1CF78294&Bank=0134&Amount=01.00"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
    except Exception as e:
        print("Error al obtener el código QR:", e)
    return None

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