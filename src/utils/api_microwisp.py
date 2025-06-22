from flask import session
from src.routes.home_bp.templates.form_fields import User
from src.utils.logger import logger
from flask_login import login_user
import src.utils.connect_api as connect_api
import os


class Client:
    def __init__(self, cedula):
        self.cedula = cedula

    def buscar_cliente(self, client_email):
        headers = {"content-type": "application/json"}
        body = {"token": os.getenv("TOKEN_MW"), "cedula": self.cedula}
        endpoint = os.getenv("ENDPOINT_BASE") + os.getenv("ENDPOINT_BUSCAR_CLIENTE")
        params = {}

        data_cliente = connect_api.conectar(headers, body, params, endpoint, "POST", self.cedula)
        if data_cliente[0]:
            if data_cliente[1]["estado"] == "exito":  # Cliente obtenido
                ###### VALIDO EL CORREO DEL CLIENTE ######
                email_mw = data_cliente[1]['datos'][0]['correo']
                if client_email.lower() == email_mw.lower():
                    # Almaceno la session
                    session.permanent = True  # Permite utilizar el tiempo de vida de la session
                    datos_cliente = {"nombre": data_cliente[1]["datos"][0]["nombre"],
                                     "id": data_cliente[1]["datos"][0]["id"],
                                     "cedula": data_cliente[1]["datos"][0]["cedula"],
                                     "estado": data_cliente[1]["datos"][0]["estado"],
                                     "movil": data_cliente[1]["datos"][0]["movil"],
                                     "facturas_nopagadas": data_cliente[1]["datos"][0]["facturacion"][
                                         "facturas_nopagadas"],
                                     "total_facturas": data_cliente[1]["datos"][0]["facturacion"]["total_facturas"]
                                     }
                    session["datos_cliente"] = datos_cliente
                    user = User(self.cedula, datos_cliente)
                    login_user(user)
                    return True, data_cliente
                else:
                    logger.error("USER: " + str(self.cedula) + " TYPE: No coinciden los correos " + "\n")
                    return False, "Error - No existe el cliente con el filtro indicado."
            elif data_cliente[1]["estado"] == "error":
                error = data_cliente[1]["mensaje"]
                return False, f"Error - {error}"
            else:
                return False, "Error - Error buscando cliente"
        else:
            return False, data_cliente[1]

