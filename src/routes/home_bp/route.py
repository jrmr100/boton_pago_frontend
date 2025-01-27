from flask import render_template, Blueprint, session
from src.routes.home_bp.templates.form_fields import FormFields
import src.config as config
import logging
from dotenv import load_dotenv
import os

# Creo mi logging del modulo
logger = logging.getLogger(__name__)

nombre_ruta = "home"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/'
)


# ############MOSTRAR HOME################
@blue_ruta.route('/', methods=["GET", "POST"])
def home():
    form = FormFields()

    # Carga de los tipos CI/RIF
    form.field2.choices = config.lista_id

    if form.validate_on_submit():
        # Obtengo los datos del formulario
        client_email = form.field1.data
        client_tipo_id = form.field2.data
        client_id = form.field3.data

        # Almaceno en la session los datos introducidos
        session["client_email"] = client_email
        session["client_id"] = client_id

        ################ Conecto con MW ##############
        token_mw = os.getenv("TOKEN_MW")
        dict_attr = {"token": token_mw, "cedula": client_id}

        print(dict_attr)
        # mwisp_var = ConnectMwisp(dict_attr, "GetClientsDetails")
        # response_client = mwisp_var.conectar_mwisp()



    #else:
    #    print(form.errors)



    return render_template("webpage.html", form=form)
