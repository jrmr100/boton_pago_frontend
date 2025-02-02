# Modulo realizado por Jhon Monrroy
# jrmr100@gmail
# OBJETIVO: Enviar correos desde IFX
# ALGORTIMO:
# Recibe la ubicacion del archivo y lista con 
# los campos a buscar, retorna lista (separada con "|")
#  con los datos encontrados 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
# importamos librerias para adjuntar
from email.mime.base import MIMEBase
from email import encoders


def enviar_correo(correo_destino, subject_email, cuerpo_correo):
    try:
        # Configuro los datos del correo
        addr_to = correo_destino
        addr_from = os.getenv("ADDR_FROM")
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")

        # Construimos el mail
        msg = MIMEMultipart()
        msg['To'] = addr_to
        msg['From'] = addr_from
        msg['Subject'] = subject_email
        # cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
        msg.attach(MIMEText(cuerpo_correo, 'plain'))

        """
        # cargamos el archivo a adjuntar
        fp = open(nombre_reporte + today + ".txt", 'rb')
        adjunto = MIMEBase('multipart', 'encrypted')
        # lo insertamos en una variable
        adjunto.set_payload(fp.read()) 
        fp.close()  
        # lo encriptamos en base64 para enviarlo
        encoders.encode_base64(adjunto) 
        # agregamos una cabecera y le damos un nombre al archivo que adjuntamos puede ser el mismo u otro
        adjunto.add_header('Content-Disposition', 'attachment', filename=nombre_reporte + today + ".txt")
        # adjuntamos al mensaje
        msg.attach(adjunto) 
        """

        # inicializamos el stmp para hacer el envio
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        # logeamos con los datos ya seteados en la parte superior
        server.login(smtp_user, smtp_pass)
        # el envio
        server.sendmail(addr_from, addr_to, msg.as_string())
        # apagamos conexion stmp
        server.quit()

        return "Correo enviado exitosamente"
    except Exception as e:
        return "Error al enviar el correo: " + str(e)

