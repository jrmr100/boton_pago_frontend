from dotenv import load_dotenv
import os
import datetime
import requests
import json




# Cargo las variables de entorno previo a mis modulos
app_dir = os.path.join(os.path.dirname(__file__))
load_dotenv(app_dir + "/.env")

from utils.enviar_correo import enviar_correo
from utils.logger import logger, now
import config as config


fecha_actual: str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
today = now.strftime('%Y%m%d')  # Requerido en este formato para validar el pago

def conectar(headers, body, params, endpoint, metodo, cedula):
    try:
        if metodo == "GET":
            logger.debug(f"USER: {cedula} - Solicitud a la API: {endpoint}\n"
                         f" - Header: {headers}"
                         f" - Body: {body}"
                         f" - params: {params}"
                         f" - Metodo: {metodo}\n")

            response = requests.get(endpoint,
                                    headers=headers,
                                    params=params,
                                    timeout=15)
        elif metodo == "POST":
            logger.debug(f"USER: {cedula} - Solicitud a la API: {endpoint}\n"
                         f" - Header: {headers}"
                         f" - Body: {body}"
                         f" - params: {params}"
                         f" - Metodo: {metodo}\n")
            response = requests.post(endpoint,
                                     headers=headers, json=body, params=params,
                                     timeout=15)

        response_decode = response.content.decode("utf-8")
        api_response = json.loads(response_decode)
        logger.debug(f"USER: {cedula} - Respuesta de la API: {endpoint}\n"
                     f" - Respuesta: {str(api_response)}\n")
        return "success", api_response
    except Exception as error:
        logger.debug(f"USER: {cedula} - Except de la API: {endpoint}\n"
                     f" - Except: {str(error)}\n")
        return "except", str(error)

def buscar_tasabcv():
    archivo_tasa = os.getenv("PATH_BASE") + os.getenv("FILE_TASABCV")
    headers = {
        'apikey': os.getenv("APIKEY_VIPPO"),
        'accountMerchant': os.getenv("ACCOUNT_VIPPO")
    }
    body = {}
    params = {}
    endpoint = os.getenv("ENDPOINT_TASABCV")

    # Busco la tasa usando el modulo conectar
    api_response = conectar(headers, body, params, endpoint, "GET", "crontab")
    if api_response[0] == "success":
        try:
            logger.info("USER: Crontab - Respuesta obtenida de tasa BCV " + str(api_response[1]))
            tasa_bcv = str(api_response[1]["result"]["bcvRates"]["rates"]['us_dollar'])
            if float(tasa_bcv) > 0:
                with open(archivo_tasa, "w", encoding="utf-8") as archivo:
                    archivo.write(tasa_bcv + ", " + fecha_actual)

                print("Tasa BCV obtenida con exito: " + tasa_bcv)
                return tasa_bcv
            else:
                print("Error obteniendo tasa BCV: " + str(api_response[1]))
                logger.error("USER: Crontab - TYPE: json con tasa BCV no es el valor esperado:" + str(api_response[1]))

                # Envio el correo con la alerta
                envio = ""
                for email in config.correos_tasa_bcv:
                    envio = enviar_correo(email,
                                          "ERROR EN BOTON DE PAGO 2NET: tasa BCV",
                                          fecha_actual + "\n" + "Tasa BCV incorrecta: " + str(api_response[1]))
                    logger.debug("USER: Crontab - Envio de correo de alerta tasa_bcv: " + str(envio))

                return None
        except Exception as error:
            print("Except obteniendo tasa BCV: " + str(error))
            logger.error("USER: Crontab - TYPE: except, error de datos recibidos de tasa BCV:" + str(error))
            # Envio el correo con la alerta
            envio = ""
            for email in config.correos_tasa_bcv:
                envio = enviar_correo(email,
                                      "ERROR EN BOTON DE PAGO 2NET: tasa BCV",
                                      fecha_actual + "\n" + "Tasa BCV incorrecta: " + str(error))
                logger.debug("USER: Crontab - Envio de correo de alerta tasa_bcv: " + str(envio))
            return "except", str(error)
    else:
        print("Error obteniendo tasa BCV: " + str(api_response[1]))
        logger.error("Error al buscar la tasa BCV en VIPPO: " + str(api_response[1]))
        # Envio el correo con la alerta
        envio = ""
        for email in config.correos_tasa_bcv:
            envio = enviar_correo(email,
                                  "ERROR EN BOTON DE PAGO 2NET: tasa BCV",
                                  fecha_actual + "\n" + "Tasa BCV incorrecta: " + str(api_response[1]))
            logger.debug("USER: Crontab - Envio de correo de alerta tasa_bcv: " + str(envio))
        return None

def buscar_listabancos_vippo():
    archivo_lista_bancos = os.getenv("PATH_BASE") + os.getenv("FILE_LISTABANCOS_VIPPO")
    endpoint = os.getenv("ENDPOINT_BASE_VIPPO") + os.getenv("URL_BANCOS_VIPPO")
    headers = {
        'apikey': os.getenv("APIKEY_VIPPO"),
        'accountMerchant': os.getenv("ACCOUNT_VIPPO")
    }
    body = {}
    params = {}

    # Busco la lista de bancos usando el modulo conectar
    api_response = conectar(headers, body, params, endpoint, "GET", "crontab")
    lista_bancos = []
    if api_response[0] == "success":
        try:
            logger.info("USER: Crontab - TYPE: Respuesta obtenida de lista de bancos:" + str(api_response[1]))
            for banks in api_response[1]["result"]["banks"]:
                lista_bancos.append(banks["codigo"] + " - " + banks["nombre"])
            lista_bancos_sorted = sorted(lista_bancos)
            with open(archivo_lista_bancos, "w", encoding="utf-8") as archivo:
                for banco in lista_bancos_sorted:
                    archivo.write(banco + "\n")
            print("Lista de bancos vippo obtenida con exito: " + str(api_response[1]))
        except Exception as error:
            print("Except obteniendo lista de bancos vippo: " + str(error))
            logger.error("USER: Crontab - TYPE: except, error de datos recibidos de lista de bancos:" + str(error))
            # Envio el correo con la alerta
            envio = ""
            for email in config.correos_tasa_bcv:
                envio = enviar_correo(email,
                                      "ERROR EN BOTON DE PAGO 2NET: lista de bancos",
                                      fecha_actual + "\n" + "Lista de bancos incorrecta: " + str(error))
                logger.debug("USER: Crontab - Envio de correo de alerta lista de bancos: " + str(envio))
            return "except", str(error)
    else:
        print("Error obteniendo lista de bancos vippo: " + str(api_response[1]))
        logger.error("USER: Crontab - Error al buscar la lista de bancos en VIPPO: " + str(api_response[1]))
        # Envio el correo con la alerta
        envio = ""
        for email in config.correos_tasa_bcv:
            envio = enviar_correo(email,
                                  "ERROR EN BOTON DE PAGO 2NET: lista de bancos",
                                  fecha_actual + "\n" + "Lista de bancos incorrecta: " + str(api_response[1]))
            logger.debug("USER: Crontab - Envio de correo de alerta lista de bancos: " + str(envio))
        return None



# se debe crear un crontab para q se ejecute de lun a vie cada 4hrs
# sudo crontab -e
# 0 1,5,9,13,17 * * 1-5 cd /var/www/boton_pago/src/utils && sudo -u www-data venv/bin/python3 crontab.py

# Obtener la tasa BCV desde vippo
buscar_tasabcv()

# Obtener lista de bancos VIPPO
buscar_listabancos_vippo()


