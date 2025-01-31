import requests
import json
import logging


logger = logging.getLogger(__name__)


def conectar(headers, body, endpoint):
    try:
        response = requests.post(endpoint,
                                 headers=headers, json=body,
                                 timeout=15)
        response_decode = response.content.decode("utf-8")
        api_response = json.loads(response_decode)
        return "success", api_response
    except Exception as error:
        logger.error("connect_api no pudo conectarse al endpoint: " + endpoint +
                     " TYPE: except " + str(error) + "\n")
        return "except", str(error)