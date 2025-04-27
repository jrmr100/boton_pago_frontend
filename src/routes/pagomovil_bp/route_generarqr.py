from flask import  Blueprint, jsonify
import requests
from flask_login import login_required
import os


nombre_ruta = "qr_ip"
nombre_ruta_con_parametro = f"{nombre_ruta}/<float:amount>"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


@blue_ruta.route('/' + nombre_ruta_con_parametro, methods=["GET", "POST"])
@login_required
def generarqr(amount):
    publickeyid = os.getenv("PUBLICKEYID_IP")
    keyid = os.getenv("KEYID_IP")
    bank = os.getenv("RECEIPTBANK_IP")
    amount = amount

    url = f"https://merchant.instapago.com/services/api/v2/Payments/GetPaymentAffiliateQR?PublicKeyId={publickeyid}&KeyId={keyid}&Bank={bank}&Amount={amount}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            qr_image = data.get("qrCode", None)
            return jsonify({"qr_image": qr_image})
        else:
            return jsonify({"qr_image": None})
    except Exception as e:
        return jsonify({"qr_image": None})

