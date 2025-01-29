from flask import render_template, Blueprint, session, redirect, url_for, flash
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
        logger.info("user: " + str(client_id) +
                    " TYPE: Iniciando transaccion\n")
        info_cliente = ApiMw(client_id)
        datos_cliente = info_cliente.buscar_cliente()

        if datos_cliente[0] == "except":
            return render_template("error_general.html", msg="Error API - MW", error=datos_cliente[1], type="503")
        elif datos_cliente[1]["estado"] == "exito":
                nro_cta = datos_cliente[1]['datos'][0]['id']
                session["nro_cta"] = nro_cta

                # Obtenemos el valor de correo para compararlo con el introducido
                email_mw = datos_cliente[1]['datos'][0]['correo']
                if client_email == email_mw:
                    return redirect(url_for('pagos.pagos'))
                else:
                    flash("No existe cliente con los datos suministrados", "failure")
        else:
            flash("No existe cliente con los datos suministrados", "failure")

    #else:
    #    print(form.errors)



    return render_template("home.html", form=form)

# TODO: logger
# TODO: Capturar errores
# TODO: Presentar Mensajes de error en pantalla
# TODO: Contextos en caso de no if
# TODO: Se podra iniciar desde MW exclusivamente -sacar CI del MW
# TODO: Colocar spinner indicando en proceso

