import requests
import json
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv()


def connect_mw(headers, body, endpoint, client_id):
    try:
        response = requests.post(endpoint,
                                 headers=headers, json=body,
                                 timeout=15)
        response_decode = response.content.decode("utf-8")
        datos_response = json.loads(response_decode)
        return "success", datos_response
    except Exception as error:
        logger.error("user: " + str(client_id) +
                    " TYPE: except " + str(error))
        return "except", str(error)


class ApiMw:
    def __init__(self, client_id):
        self.client_id = client_id

    def buscar_cliente(self):
        headers = {"content-type": "application/json"}
        body = {"token": os.getenv("TOKEN_MW"), "cedula": self.client_id}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_CLIENTE")

        cliente = connect_mw(headers, body, endpoint, self.client_id)
        return cliente
