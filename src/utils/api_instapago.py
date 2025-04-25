import requests


def generar_qr():
    url = "https://merchant.instapago.com/services/api/v2/Payments/GetPaymentAffiliateQR?PublicKeyId=e46dc9c8ce04bccfd742322b3ccc9049&KeyId=890AB86E-5938-4CEB-BC37-CA8C1CF78294&Bank=0134&Amount=01.00"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("qrCode", None)  # Extraemos el campo qrCode
    except Exception as e:
        print("Error al obtener el código QR:", e)
    return None