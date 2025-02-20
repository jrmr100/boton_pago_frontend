import os
import src.utils.connect_api as connect_api
from src.utils.logger import now

today = now.strftime('%Y%m%d%H%M%S')


def buscar_cliente(client_id):
    headers = {"content-type": "application/json"}
    body = {"token": os.getenv("TOKEN_MW"), "cedula": client_id}
    endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_CLIENTE")

    api_response = connect_api.conectar(headers, body, endpoint, "POST")
    return api_response

def buscar_facturas(id_cliente, monto_pagado_bs, monto_deuda):
    # Valido la longitud del ID del cliente
    if len(id_cliente) < 1 or len(id_cliente) > 7:
        return "error", "idtraza muy largo"

        # Valido si el monto pagado es inferior a la deuda
    elif float(monto_pagado_bs) < float(monto_deuda):
        return "error", "El monto pagado (Bs." + monto_pagado_bs + ") esta por debajo de la deuda (Bs." + str(monto_deuda) + ")"
    else:
        # Obtengo los codigos de las facturas pendientes por el cliente
        headers = {}
        body = {"token": os.getenv("TOKEN_MW"), "idcliente": id_cliente, "estado": "1"}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_FACTURAS")
        api_response = connect_api.conectar(headers, body, endpoint, "POST")
        return api_response

def pagar_facturas(facturas, codigo_auth, medio_pago):
    cod_factura = 1
    headers = {"Content-Type": "application/json"}
    endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_PAGAR")

    for factura in facturas:
        body = {"token": os.getenv("TOKEN_MW"),
                   "idfactura": factura["id"],
                   "pasarela": "API-" + medio_pago,
                   "idtransaccion": codigo_auth + "-" + today + "-" + str(cod_factura)}
        api_response = connect_api.conectar(headers, body, endpoint, "POST")
        cod_factura = cod_factura + 1

    return api_response

