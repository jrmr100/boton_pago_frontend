import requests
import json
from src.utils.logger import logger


def conectar(headers, body, params, endpoint, metodo, cedula):
    try:
        if metodo == "GET":
            logger.debug(f"USER: {cedula} - Solicitud a la API: {endpoint}"
                         f" - Header: {headers}"
                         f" - Body: {body}"
                         f" - params: {params}"
                         f" - Metodo: {metodo}\n")


            response = requests.get(endpoint,
                                    headers=headers,
                                    params=params,
                                    timeout=30)
        elif metodo == "POST":
            logger.debug(f"USER: {cedula} - Solicitud a la API: {endpoint}"
                         f" - Header: {headers}"
                         f" - Body: {body}"
                         f" - params: {params}"
                         f" - Metodo: {metodo}\n")

            response = requests.post(endpoint,
                                     headers=headers, json=body, params=params,
                                     timeout=30)

        response_decode = response.content.decode("utf-8")
        api_response = json.loads(response_decode)
        logger.debug(f"USER: {cedula} - Respuesta de la API: {endpoint}"
                     f" - Respuesta: {str(api_response)}\n")
        return "success", api_response
    except Exception as error:
        logger.debug(f"USER: {cedula} - Except de la API: {endpoint}"
                     f" - Except: {str(error)}\n")
        return "except", str(error)
