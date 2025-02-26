from flask import render_template, Blueprint, session, redirect, url_for, flash
from src.routes.home_bp.templates.form_fields import FormFields
from src.utils.api_mw import buscar_cliente
import src.config as config
from src.utils.logger import logger
import src.routes.home_bp.validaciones_home as validaciones_home
from flask_login import login_required, logout_user, login_user
from src.routes.home_bp.templates.form_fields import User


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

        ################ Busco cliente en MW ##############
        logger.info("user: " + str(client_id) +
                    " TYPE: Iniciando transacción con el correo: " + client_email + "\n")
        resultado_apimw = buscar_cliente(client_id)
        logger.debug("user: " + str(client_id) +
                    " TYPE: resultado de la busqueda de cliente: " + str(resultado_apimw) + "\n")

        ############ VALIDO LA RESPUESTA DE MW ############
        if resultado_apimw[0] == "success":
            if resultado_apimw[1]["estado"] == "exito":
                ###### VALIDO EL CORREO DEL CLIENTE ######
                email_mw = resultado_apimw[1]['datos'][0]['correo']
                if client_email == email_mw:
                    total_facturas = resultado_apimw[1]["datos"][0]["facturacion"]["total_facturas"]
                    if float(total_facturas) > 0:
                        #### USUARIO AUTENTICADO ####
                        user = User(client_id)
                        login_user(user)
                        session.permanent = True  # Permite utilizar el tiempo de vida de la session
                        session["nombre"] = resultado_apimw[1]["datos"][0]["nombre"]
                        session["id"] = resultado_apimw[1]["datos"][0]["id"]
                        session["cedula"] = resultado_apimw[1]["datos"][0]["cedula"]
                        session["estado"] = resultado_apimw[1]["datos"][0]["estado"]
                        session["PlanContratado"] = resultado_apimw[1]["datos"][0]["PlanContratado"]
                        session["facturas_nopagadas"] = resultado_apimw[1]["datos"][0]["facturacion"]["facturas_nopagadas"]
                        session["datos_cliente"] = resultado_apimw[1]


                        return redirect(url_for('pagos.pagos'))
                    else:
                        flash("No tiene facturas pendientes para cancelar", "sucess")
                else:
                    logger.error("user: " + str(client_id) +
                                 " TYPE: correo no iguales\n")
                    flash("No existe cliente con los datos suministrados", "failure")
            else:
                validar_resultado_apimw = validaciones_home.resultado_apimw(resultado_apimw)
                if validar_resultado_apimw[0] == "flash":
                    logger.error("user: " + str(client_id) +
                                 " TYPE: " + validar_resultado_apimw[1] + "\n")
                    flash(validar_resultado_apimw[1], "failure")
                elif validar_resultado_apimw[0] == "error_page":
                    logger.error("user: " + str(client_id) +
                                 " TYPE: Error API - MW: " + str(resultado_apimw[1]) + "\n")
                    return render_template("error_general.html", msg="Error API - MW", error=validar_resultado_apimw[1],
                                           type="503")
        else:
            validar_resultado_apimw = validaciones_home.resultado_apimw(resultado_apimw)
            if validar_resultado_apimw[0] == "error_page":
                logger.error("user: " + str(client_id) +
                             " TYPE: Error API - MW: " + str(resultado_apimw[1]) + "\n")
                return render_template("error_general.html", msg="Error API - MW", error=validar_resultado_apimw[1],
                                       type="503")

    return render_template("home.html", form=form)

@blue_ruta.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))