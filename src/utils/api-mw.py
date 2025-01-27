import requests
import json
import src.config as config
import logging

logger = logging.getLogger(__name__)

class MwConnect:
    def __init__(self, dict_attr, endpoint_end):
        self.dict_attr = dict_attr
        self.end_point = config.endpoint_mikrowisp
        self.end_point_end = endpoint_end

    def conectar_mwisp(self):
        payload = self.dict_attr
        cabecera = {"content-type": "application/json"}

        try:
            logger.debug("Enviando a MW: " + str(payload) + " / endpoint: " + self.end_point + self.end_point_end)
            response = requests.post(self.end_point + self.end_point_end,
                                     headers=cabecera, json=payload,
                                     timeout=15)
            response_decode = response.content.decode("utf-8")
            datos_response = json.loads(response_decode)
            return datos_response
        except Exception as e:
            logger.debug("TYPE: Exception de conectar_mwisp/ " + str(e))
            return "error_connectmw"