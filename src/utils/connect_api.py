import requests
import json


def conectar(headers, body, endpoint, metodo):
    try:
        if metodo == "GET":
            response = requests.get(endpoint,
                                    headers=headers,
                                    timeout=15)
        elif metodo == "POST":
            response = requests.post(endpoint,
                                     headers=headers, json=body,
                                     timeout=15)

        response_decode = response.content.decode("utf-8")
        api_response = json.loads(response_decode)
        return "success", api_response
    except Exception as error:
        return "except", str(error)