from dotenv import load_dotenv
from src.utils.logger import logger, now
from src.utils.enviar_correo import enviar_correo
import os
import src.utils.connect_api as connect_api
import src.config as config
import datetime
from flask_login import current_user

load_dotenv()
fecha_actual: str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
today = now.strftime('%Y%m%d')  # Requerido en este formato para validar el pago


def buscar_tasabcv():
    archivo_tasa = os.getenv("PATH_BASE") + os.getenv("FILE_TASABCV")
    headers = {
        'apikey': os.getenv("APIKEY_VIPPO"),
        'accountMerchant': os.getenv("ACCOUNT_VIPPO")
    }
    body = {}
    endpoint = os.getenv("ENDPOINT_TASABCV")

    # Busco la tasa usando el modulo conectar
    api_response = connect_api.conectar(headers, body, endpoint, "GET", "crontab")
    if api_response[0] == "success":
        try:
            logger.info("Respuesta obtenida de tasa BCV " + str(api_response[1]))
            tasa_bcv = str(api_response[1]["result"]["bcvRates"]["rates"]['us_dollar'])
            if float(tasa_bcv) > 0:
                with open(archivo_tasa, "w") as archivo:
                    archivo.write(tasa_bcv + ", " + fecha_actual)

                return tasa_bcv
            else:
                logger.error("TYPE: json con tasa BCV no es el valor esperado:" + str(api_response[1]))

                # Envio el correo con la alerta
                envio = ""
                for email in config.correos_tasa_bcv:
                    envio = enviar_correo(email,
                                          "ERROR EN BOTON DE PAGO 2NET: tasa BCV",
                                          fecha_actual + "\n" + "Tasa BCV incorrecta: " + str(api_response[1]))
                    logger.debug("Envio de correo de alerta tasa_bcv: " + str(envio))

                return None
        except Exception as error:
            logger.error("TYPE: except, error de datos recibidos de tasa BCV:" + str(error))
            # Envio el correo con la alerta
            envio = ""
            for email in config.correos_tasa_bcv:
                envio = enviar_correo(email,
                                      "ERROR EN BOTON DE PAGO 2NET: tasa BCV",
                                      fecha_actual + "\n" + "Tasa BCV incorrecta: " + str(error))
                logger.debug("Envio de correo de alerta tasa_bcv: " + str(envio))
            return "except", str(error)
    else:
        logger.error("Error al buscar la tasa BCV en VIPPO: " + str(api_response[1]))
        # Envio el correo con la alerta
        envio = ""
        for email in config.correos_tasa_bcv:
            envio = enviar_correo(email,
                                  "ERROR EN BOTON DE PAGO 2NET: tasa BCV",
                                  fecha_actual + "\n" + "Tasa BCV incorrecta: " + str(api_response[1]))
            logger.debug("Envio de correo de alerta tasa_bcv: " + str(envio))
        return None


def leer_tasa_bcv():
    # Funcion llamada desde el programa y busca la tasa en el archivo tasa_bcv.txt
    try:
        # Leer la tasa desde el archivo tasa_bcv.txt
        with open(os.getenv("PATH_BASE") + os.getenv("FILE_TASABCV"), 'r') as archivo:
            lineas_tasa_bcv = archivo.read()
        lista_tasa_bcv = lineas_tasa_bcv.split(",")
        tasa_bcv = lista_tasa_bcv[0]
        logger.debug("USER: " + current_user.id + " - Tasa BCV leida del archivo TXT: " + str(tasa_bcv) + "\n")
        return tasa_bcv
    except Exception as e:
        logger.debug("USER: " + current_user.id + " - Except de la lectura de tasa BCV desde el archivo: " + str(e) + "\n")
        return "error tasa_bcv:" + str(e)


def buscar_listabancos():
    archivo_lista_bancos = os.getenv("PATH_BASE") + os.getenv("FILE_LISTABANCOS")
    endpoint = os.getenv("ENDPOINT_BASE_VIPPO") + os.getenv("URL_BANCOS")
    headers = {
        'apikey': os.getenv("APIKEY_VIPPO"),
        'accountMerchant': os.getenv("ACCOUNT_VIPPO")
    }
    body = {}

    # Busco la lista de bancos usando el modulo conectar
    api_response = connect_api.conectar(headers, body, endpoint, "GET", "crontab")
    lista_bancos = []
    if api_response[0] == "success":
        try:
            logger.info("TYPE: Respuesta obtenida de lista de bancos:" + str(api_response[1]))
            for banks in api_response[1]["result"]["banks"]:
                lista_bancos.append(banks["codigo"] + " - " + banks["nombre"])
            lista_bancos_sorted = sorted(lista_bancos)
            with open(archivo_lista_bancos, "w") as archivo:
                for banco in lista_bancos_sorted:
                    archivo.write(banco + "\n")
        except Exception as error:
            logger.error("TYPE: except, error de datos recibidos de lista de bancos:" + str(error))
            # Envio el correo con la alerta
            envio = ""
            for email in config.correos_tasa_bcv:
                envio = enviar_correo(email,
                                      "ERROR EN BOTON DE PAGO 2NET: lista de bancos",
                                      fecha_actual + "\n" + "Lista de bancos incorrecta: " + str(error))
                logger.debug("Envio de correo de alerta lista de bancos: " + str(envio))
            return "except", str(error)
    else:
        logger.error("Error al buscar la lista de bancos en VIPPO: " + str(api_response[1]))
        # Envio el correo con la alerta
        envio = ""
        for email in config.correos_tasa_bcv:
            envio = enviar_correo(email,
                                  "ERROR EN BOTON DE PAGO 2NET: lista de bancos",
                                  fecha_actual + "\n" + "Lista de bancos incorrecta: " + str(api_response[1]))
            logger.debug("Envio de correo de alerta lista de bancos: " + str(envio))
        return None


def leer_listabancos():
    # Funcion llamada desde el programa y busca la tasa en el archivo lista_bancos.txt
    try:
        # Leer la lista de bancos
        with open(os.getenv("PATH_BASE") + os.getenv("FILE_LISTABANCOS"), 'r') as archivo:
            linea_lista_bancos = archivo.read()
            lista_bancos = linea_lista_bancos.split("\n")
            logger.debug("USER: " + current_user.id + " - Lista de bancos leida del archivo TXT: " + str(lista_bancos) + "\n")
            return lista_bancos
    except Exception as e:
        logger.debug("USER: " + current_user.id + " - Except de la lectura de la lista de bancos desde el archivo: " + str(e) + "\n")
        return "error listabancos - " + str(e)


def validar_pago(id_customer, phone_payer, entity, order, montobs):
    endpoint = os.getenv("ENDPOINT_BASE_VIPPO") + os.getenv("URL_VALIDATE")

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
                    "startDate": today,
                    "endDate": today,
                },
                "customerID": id_customer,
                "customerPhone": phone_payer,
                "entity": entity,
                "reference": order,
                "bill": os.getenv("BILL"),
                "amount": montobs,
            }
            }
    api_response = connect_api.conectar(headers, body, endpoint, "POST", current_user.id)
    if api_response[0] == "success":
            return "success", api_response[1]
    elif api_response[0] == "except":
        return "except", api_response[1]
