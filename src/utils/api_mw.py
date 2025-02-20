import os
import src.utils.connect_api as connect_api
from src.utils.logger import logger




def buscar_cliente(client_id):
    headers = {"content-type": "application/json"}
    body = {"token": os.getenv("TOKEN_MW"), "cedula": client_id}
    endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_CLIENTE")

    api_response = connect_api.conectar(headers, body, endpoint, "POST")
    return api_response

def buscar_facturas(id_cliente, monto_pagado_bs, monto_deuda):
    # Valido la longitud del ID del cliente
    if len(id_cliente) < 1 or len(id_cliente) > 7:
        logger.error("user: " + str(id_cliente) +
                     " TYPE: Error en IdTraza - muy largo")
        return "error", "idtraza muy largo"

        # Valido si el monto pagado es inferior a la deuda
    elif float(monto_pagado_bs) < float(monto_deuda):
        logger.error("user: " + str(id_cliente) +
                     " TYPE: Monto pagado inferior a la deuda")
        return "error", "El monto pagado (Bs." + monto_pagado_bs + ") esta por debajo de la deuda (Bs." + str(monto_deuda) + ")"
    else:
        # Obtengo los codigos de las facturas pendientes por el cliente
        headers = {"content-type": "application/json", "token": os.getenv("TOKEN_MW"), "idcliente": id_cliente, "estado": "1"}
        body = {}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_FACTURAS")
        api_response = connect_api.conectar(headers, body, endpoint, "POST")
        logger.debug("user: " + str(id_cliente) +
                     " TYPE: Respuesta MW buscando facturas: " + str(api_response))

        return "success", api_response
