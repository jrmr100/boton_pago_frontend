from flask import render_template, Blueprint, session, redirect, url_for
from src.utils.api_mw import ApiMw
import src.config as config
import logging
from dotenv import load_dotenv
import os

# Creo mi logging del modulo
logger = logging.getLogger(__name__)

nombre_ruta = "pagos"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


# ############MOSTRAR HOME################
@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
def pagos():


    #else:
    #    print(form.errors)



    return render_template("pagos.html")

