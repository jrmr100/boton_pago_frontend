import requests
from requests.exceptions import RequestException, HTTPError
import json
from src.utils.logger import logger


def conectar(headers, body, params, endpoint, metodo, cedula):
    try:
        response = None
        logger.debug(f"USER: {cedula} - Solicitud a la API: {endpoint}"
                     f" - Header: {headers}"
                     f" - Body: {body}"
                     f" - params: {params}"
                     f" - Metodo: {metodo}\n")
        if metodo == "GET":
            response = requests.get(endpoint,
                                    headers=headers,
                                    params=params,
                                    timeout=30)
            response.raise_for_status()
        elif metodo == "POST":
            response = requests.post(endpoint,
                                     headers=headers, json=body, params=params,
                                     timeout=30)
            response.raise_for_status()

        try:
            response_decode = response.content.decode("utf-8")
            api_response = json.loads(response_decode)
            logger.debug(f"USER: {cedula} - Respuesta de la API: {endpoint}"
                         f" - Respuesta: {str(api_response)}\n")
            return True, api_response
        except ValueError:
            logger.debug(f"USER: {cedula} - Except de la API: {endpoint}"
                         f" - Except-json: Error en JSON de respuesta\n")
            return False, f"Except de la API: {endpoint} - Error en JSON de respuesta"
    except HTTPError as http_err:
        # Captura errores HTTP (4xx o 5xx) que el servidor envió.
        logger.debug(f"USER: {cedula} - Except de la API: {endpoint}"
                     f" - Except-http: {str(http_err)}\n")
        return False, http_err
    except RequestException as req_err:
        # Captura errores de conexión (ej. DNS, red inaccesible, timeout, URL incorrecta).
        logger.debug(f"USER: {cedula} - Except de la API: {endpoint}"
                     f" - Except-req: {str(req_err)}\n")
        return False, req_err
    except Exception as error:
        logger.debug(f"USER: {cedula} - Except de la API: {endpoint}"
                     f" - Except: {str(error)}\n")
        return False, error
