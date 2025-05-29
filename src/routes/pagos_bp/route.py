from flask import render_template, Blueprint, session, redirect, url_for, flash
from src.utils.api_vippo import leer_tasa_bcv
from src.routes.pagos_bp.templates.form_fields import FormFields
from flask_login import login_required, current_user
import src.config as config


nombre_ruta = "pagos"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)

# Cargo la lista de bancos solo una vez cuando se acceda a la ruta pagomovil
tasa_bcv = None


@blue_ruta.before_request
@login_required
def cargar_tasa_bcv():
    global tasa_bcv
    if tasa_bcv is None:
        tasa_bcv = leer_tasa_bcv()
        if "error tasa_bcv" in tasa_bcv:
            return render_template("error_general.html", msg="Error obteniendo tasa BCV, intente mas tarde",
                                   error="No es posible acceder al valor de la tasa BCV", type="500")



@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
@login_required
def pagos():
    form = FormFields()
    datos_cliente = current_user.datos_cliente
    session["tasa_bcv"] = tasa_bcv

    # VALIDO CONDICIONES DEL CLIENTE
    if datos_cliente["estado"] == "RETIRADO":
        card_disable = True
        flash("Cuenta \"RETIRADA\" debe contactar a nuestro centro de atención por WhatsApp - " +
              config.contacto_WhatsApp, "failure")
    elif float(datos_cliente["total_facturas"]) <= 0:
        card_disable = True
        flash("La cuenta no presenta deudas", "info")
    else:
        card_disable = False


    # Calculo el monto en Bs
    monto_dls = float(datos_cliente["total_facturas"])
    montobs_long = float(monto_dls) * float(tasa_bcv)
    monto_bs = f"{montobs_long:.2f}"

    if form.validate_on_submit():
        if form.submit1.data:  # Si se presiona el boton de submit1
            session["monto_bs"] = monto_bs
            return redirect(url_for('pagomovil_bancos.pagomovil_bancos'))


    if float(monto_bs) > 0:
        deuda = True
    else:
        deuda = False

    return render_template("pagos.html", datos_cliente=datos_cliente,
                           monto_bs=monto_bs, form=form, monto_dls=monto_dls, card_disable=card_disable, deuda=deuda)

# TODO: Modulo de Lukapay pago movil - apagable
# TODO: Modulo de Lukapay zelle - apagable
# TODO: Validar el trackid diferido
# TODO: Se podra iniciar desde MW exclusivamente -sacar CI del MW
# TODO: Validar si se puede usar en mw el campo client_tipo_id (tipo de id)
# TODO: Agregar lista de correos en config
# TODO: Revisar responsive en todo el proyecto
# TODO: validar si es consulta o validate de pagos en instapago


