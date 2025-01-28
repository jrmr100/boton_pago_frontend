from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.home_bp.templates.form_fields import FormFields
from src.utils.api_mw import ApiMw
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

        ################ Busco cliente en MW ##############

        info_cliente = ApiMw(client_id)
        datos_cliente = info_cliente.buscar_cliente()

        if datos_cliente["estado"] == "exito":
            nro_cta = datos_cliente['datos'][0]['id']
            session["nro_cta"] = nro_cta

            # Obtenemos el valor de correo para compararlo
            email_mw = datos_cliente['datos'][0]['correo']
            if client_email == email_mw:
                return redirect(url_for('pagos.pagos'))




    #else:
    #    print(form.errors)



    return render_template("home.html", form=form)

#TODO: Terminar API de MW
#TODO: logger y errores

