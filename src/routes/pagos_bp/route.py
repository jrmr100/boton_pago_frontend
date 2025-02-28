from flask import render_template, Blueprint, session, redirect, url_for
from src.utils.api_vippo import leer_tasa_bcv
from src.utils.logger import logger
from src.routes.pagos_bp.templates.form_fields import FormFields
from flask_login import login_required, current_user
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


    # Calculo el monto en Bs
    monto_dls = float(datos_cliente["total_facturas"])
    montobs_long = float(monto_dls) * float(tasa_bcv)
    monto_bs = float("{:.2f}".format(montobs_long))

    if form.validate_on_submit():
        if form.submit1.data:  # Si se presiona el boton de submit1
            session["monto_bs"] = monto_bs
            return redirect(url_for('pagomovil.pagomovil'))

    return render_template("pagos.html", datos_cliente=datos_cliente,
                           monto_bs=monto_bs, form=form, monto_dls=monto_dls)

# TODO: Definir si usar CDN o no para los iconos de bootstrap
# TODO: Modulo de Lukapay pago movil - apagable
# TODO: Modulo de Lukapay zelle - apagable
# TODO: Icono de pestaña con temas claros
# TODO: Validar el trackid diferido
# TODO: botones en el resultado de pago?
# TODO: Mostrar monto de la deuda luego del pago exitoso?
# TODO: En home al no tener factura mostrar en gris en las opciopnes de pago
# TODO: Si esta retirado mensaje de comunicarse al callcenter y poner en gris
# TODO: Se podra iniciar desde MW exclusivamente -sacar CI del MW
# TODO: Validar si se puede usar en mw el campo client_tipo_id (tipo de id)
# TODO: Eliminar spinner al regresar en home
# TODO: que hacer con el campo plan contratado?
# TODO: Agregar lista de correos en config

