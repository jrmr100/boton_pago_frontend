from flask import render_template, Blueprint, redirect, url_for, flash
from src.routes.home_bp.templates.form_fields import FormFields
from src.utils.api_mw import buscar_cliente
import src.config as config
from src.utils.logger import logger
from flask_login import login_required, logout_user


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
    form.tipo_id.choices = config.lista_id

    if form.validate_on_submit():
        # Obtengo los datos del formulario
        client_email = form.email.data
        client_tipo_id = form.tipo_id.data  # no usado por ahora
        client_id = form.ci.data

        logger.info("USER: " + str(client_id) +
                    " TYPE: Iniciando transacción con el correo: " + client_email + "\n")

        ################ Busco cliente en MW ##############
        resultado_apimw = buscar_cliente(client_id, client_email)
        if resultado_apimw[0] == "success":
                #### USUARIO AUTENTICADO Y VALIDADO####
                return redirect(url_for('pagos.pagos'))
        elif resultado_apimw[0] == "error":
            flash(resultado_apimw[1], "failure")
        #elif resultado_apimw[0] == "info":
        #    flash(resultado_apimw[1], "info")
        elif resultado_apimw[0] == "except":
            return render_template("error_general.html", msg="Error API - MW", error=resultado_apimw[1],
                                   type="503")

    return render_template("home.html", form=form)

@blue_ruta.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))