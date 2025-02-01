from flask import render_template, Blueprint, session, redirect, url_for, flash
from src.routes.home_bp.templates.form_fields import FormFields
from src.utils.api_mw import ApiMw
import src.config as config
from src.utils.logger import logger
import src.routes.home_bp.validaciones as validaciones


nombre_ruta = "home"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/'
)

@blue_ruta.route('/', methods=["GET", "POST"])
def home():
    form = FormFields()

    # Carga de los tipos CI/RIF
    form.field2.choices = config.lista_id

    if form.validate_on_submit():
        # Obtengo los datos del formulario
        client_email = form.field1.data
        client_tipo_id = form.field2.data  # no usado por ahora
        client_id = form.field3.data

        ################ Busco cliente en MW ##############
        logger.info("user: " + str(client_id) +
                    " TYPE: Iniciando transacción con el correo: " + client_email + "\n")
        info_cliente = ApiMw(client_id)
        resultado_apimw = info_cliente.buscar_cliente()
        logger.debug("user: " + str(client_id) +
                    " TYPE: resultado de la busqueda de cliente: " + str(resultado_apimw) + "\n")

        # valido los resultados de la API
        valida_api = validaciones.resultado_api(resultado_apimw)

        if valida_api == "exito":
            # Valido el correo
            email_mw = resultado_apimw[1]['datos'][0]['correo']
            valida_email = validaciones.validar_email(client_email, email_mw)
            if valida_email is True:
                nro_cta = resultado_apimw[1]['datos'][0]['id']
                session["datos_cliente"] = resultado_apimw[1]
                return redirect(url_for('pagos.pagos'))
            else:
                logger.error("user: " + str(client_id) +
                            " TYPE: correo no iguales\n")
                flash("No existe cliente con los datos suministrados", "failure")
        elif valida_api == "except":
            return render_template("error_general.html", msg="Error API - MW", error=resultado_apimw[1], type="503")

        elif valida_api == "error":
            flash("No existe cliente con los datos suministrados", "failure")

    return render_template("home.html", form=form)

# TODO: Se podra iniciar desde MW exclusivamente -sacar CI del MW
# TODO: Colocar spinner indicando en proceso
# TODO: Validar si se puede usar en mw el campo client_tipo_id (tipo de id)

