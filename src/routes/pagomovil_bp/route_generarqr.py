from flask import  Blueprint, jsonify
from flask_login import current_user
import src.utils.connect_api as connect_api
from flask_login import login_required
import os


nombre_ruta = "generarqr"
# nombre_ruta_con_parametro = f"{nombre_ruta}/<float:amount>"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


#@blue_ruta.route('/' + nombre_ruta_con_parametro, methods=["GET", "POST"])
@blue_ruta.route('/' + nombre_ruta + '/<string:amount>', methods=["GET", "POST"])
@login_required
def generarqr(amount):
    publickeyid = os.getenv("PUBLICKEYID_IP")
    keyid = os.getenv("KEYID_IP")
    bank = os.getenv("RECEIPTBANK_IP")
    amount = str(amount)
    # amount = 90   # monto de prueba
    headers = {}
    body = {}
    params = {
        "keyId": keyid,
        "publickeyid": publickeyid,
        "bank": bank,
        "amount": amount
    }
    endpoint = os.getenv("ENDPOINT_BASE_IP") + os.getenv("URL_QR_IP")
    client_id = current_user.id

    api_response = connect_api.conectar(headers, body, params, endpoint, "GET", client_id)

    if api_response[0]:
        if api_response[1]["code"] == "200":
            qr_image = api_response[1]["qrCode"]
            return jsonify({"qr_image": qr_image})
        else:
            return jsonify({"qr_image": None})
    else:
        return jsonify({"qr_image": None})

