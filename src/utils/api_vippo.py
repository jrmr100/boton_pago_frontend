from dotenv import load_dotenv
from src.utils.logger import logger, now
import os
import src.utils.connect_api as connect_api
import datetime
from flask_login import current_user

load_dotenv()
fecha_actual: str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")



def leer_tasa_bcv():
    # Funcion llamada desde el programa y busca la tasa en el archivo tasa_bcv.txt
    try:
        # Leer la tasa desde el archivo tasa_bcv.txt
        with open(os.getenv("PATH_BASE") + os.getenv("FILE_TASABCV"), 'r', encoding="utf-8") as archivo:
            lineas_tasa_bcv = archivo.read()
        lista_tasa_bcv = lineas_tasa_bcv.split(",")
        tasa_bcv = lista_tasa_bcv[0]
        logger.debug("USER: " + current_user.id + " - Tasa BCV leida del archivo TXT: " + str(tasa_bcv) + "\n")
        return tasa_bcv
    except Exception as e:
        logger.debug("USER: " + current_user.id + " - Except de la lectura de tasa BCV desde el archivo: " + str(e) + "\n")
        return "error tasa_bcv:" + str(e)


def leer_listabancos():
    # Funcion llamada desde el programa y busca la tasa en el archivo lista_bancos.txt
    try:
        # Leer la lista de bancos
        with open(os.getenv("PATH_BASE") + os.getenv("FILE_LISTABANCOS_VIPPO"), 'r', encoding="utf-8") as archivo:
            linea_lista_bancos = archivo.read()
            lista_bancos = linea_lista_bancos.split("\n")
            logger.debug("USER: " + current_user.id + " - Lista de bancos leida del archivo TXT: " + str(lista_bancos) + "\n")
            return lista_bancos
    except Exception as e:
        logger.debug("USER: " + current_user.id + " - Except de la lectura de la lista de bancos desde el archivo: " + str(e) + "\n")
        return "error listabancos - " + str(e)


def validar_pago(id_pagador, phone_payer, entity, order, montobs, fecha_pago):
    date = fecha_pago.strftime('%Y-%m-%d')
    endpoint = os.getenv("ENDPOINT_BASE_VIPPO") + os.getenv("URL_VALIDATE")

    params = {}
    # Creo el header y el body para validar el pago movil
    headers = {"apikey": os.getenv("APIKEY_VIPPO"),
               "account": os.getenv("ACCOUNT_VIPPO")}

    # Body produccion
    body = {"branchCommerce": os.getenv("BRANCH_COMMERCE"),
            "channelCode": os.getenv("CHANNEL_CODE"),
            "issuingEntity": os.getenv("BANCO_RECEPTOR_PAGOMOVIL"),
            "ipAddress": os.getenv("IP_ADDRESS"),
            "data": {
                "dates": {
                    "startDate": date,
                    "endDate": date,
                },
                "customerID": id_pagador,
                "customerPhone": phone_payer,
                "entity": entity,
                "reference": order,
                "bill": os.getenv("BILL"),
                "amount": montobs,
            }
            }
    api_response = connect_api.conectar(headers, body, params, endpoint, "POST", current_user.id)

    if api_response[0] == "success":
            return "success", api_response[1]
    elif api_response[0] == "except":
        return "except", api_response[1]
