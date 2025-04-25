import requests
import json
from src.utils.logger import logger


def conectar(headers, body, params, endpoint, metodo, cedula):
    try:
        if metodo == "GET":
            logger.debug(
                "USER: " + cedula + " - Solicitud de API: " +
                "Header: " + str(headers) + " / " +
                "Body: " + str(body) + " / " +
                "params" + str(params) +  " / " +
                "Endpoint: " + endpoint + " / " +
                "Metodo: " + metodo + "\n")

            response = requests.get(endpoint,
                                    headers=headers,
                                    params=params,
                                    timeout=15)
        elif metodo == "POST":
            logger.debug(
                "USER: " + cedula + " - Solicitud de API: " +
                "Header: " + str(headers) + " / " +
                "Body: " + str(body) + " / " +
                "params" + str(params) + " / " +
                "Endpoint: " + endpoint + " / " +
                "Metodo: " + metodo + "\n")
            response = requests.post(endpoint,
                                     headers=headers, json=body, params=params,
                                     timeout=15)

        response_decode = response.content.decode("utf-8")
        api_response = json.loads(response_decode)
        logger.debug("USER: " + cedula + " - Respuesta de API:" + str(api_response) + "\n")
        return "success", api_response
    except Exception as error:
        logger.debug("USER: " + cedula + " - Except de conectar API:" + str(error) + "\n")
        return "except", str(error)
