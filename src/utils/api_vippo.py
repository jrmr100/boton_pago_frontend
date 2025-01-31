from sys import api_version

import requests
import json
from dotenv import load_dotenv
import os
import logging
import src.utils.connect_api as connect_api


logger = logging.getLogger(__name__)
load_dotenv()


class ApiVippo:
    def __init__(self, headers, body, endpoint):
        self.headers = headers
        self.body = body
        self.endpoint = endpoint


    def buscar_tasabcv(self):
        api_response = connect_api.conectar(self.headers, self.body, self.endpoint)
        data = api_response.json()
        tasa_bcv = str(data["result"]["bcvRates"]["rates"]['us_dollar'])

        return api_response
