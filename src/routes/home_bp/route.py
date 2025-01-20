from flask import render_template, redirect, url_for, session, Blueprint
from src.routes.home_bp.templates.form_template import FormTemplate
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
    form_template = FormTemplate()
    if form_template.validate_on_submit():
        print("Formulario enviado")

    return render_template("home.html", form_template=form_template)
