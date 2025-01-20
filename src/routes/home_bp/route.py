from flask import render_template, redirect, url_for, session, Blueprint
from wtforms import SelectField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
import logging

# Creo mi logging del modulo
logger = logging.getLogger(__name__)

nombre_ruta = "home"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    url_prefix="/"
)


# ############MOSTRAR HOME################
@blue_ruta.route('/', methods=['GET'])
def home():
    try:
       pass




    except Exception as error_home:
        logger.debug("Exception en home form " + str(error_home) + "/n")
        return render_template('error.html',
                               form_error="Error en home " + str(error_home))

    return render_template("home.html")
