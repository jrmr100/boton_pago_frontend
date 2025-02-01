from dotenv import load_dotenv
import os
import src.utils.connect_api as connect_api

load_dotenv()


class ApiMw:
    def __init__(self, client_id):
        self.client_id = client_id

    def buscar_cliente(self):
        headers = {"content-type": "application/json"}
        body = {"token": os.getenv("TOKEN_MW"), "cedula": self.client_id}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_CLIENTE")

        api_response = connect_api.conectar(headers, body, endpoint, "POST")
        return api_response
