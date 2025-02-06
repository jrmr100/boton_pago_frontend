from flask import render_template, Blueprint, session, redirect, url_for
from src.utils.api_vippo import leer_tasa_bcv
from src.utils.logger import logger
from src.routes.pagos_bp.templates.form_fields import FormFields



nombre_ruta = "pagos"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
def pagos():
    form = FormFields()

    datos_cliente = session["datos_cliente"]

    tasa_bcv = leer_tasa_bcv()
    if "error tasa_bcv" in tasa_bcv:
        logger.error("Error obteniendo la tasa BCV desde el archivo TXT: " + str(tasa_bcv) + "\n")
        return render_template("error_general.html", msg="Error obteniendo tasa BCV,"
                                                         " intente mas tarde",
                               error="No es posible acceder al valor de la tasa BCV", type="500")
    else:
        logger.info("Tasa obtenida del archivo TXT: " + str(tasa_bcv))

    # Calculo el monto en Bs
    montodls = datos_cliente["datos"][0]["facturacion"]["total_facturas"]
    montobs_long = float(montodls) * float(tasa_bcv)
    monto_bs = "{:.2f}".format(montobs_long)

    if form.validate_on_submit():
        if form.submit1.data:
            return redirect(url_for('pagomovil.pagomovil'))
        if form.submit2.data:
            return redirect(url_for('zelle.zelle'))
    # Obtengo la tasa BCV desde la funcion







    return render_template("pagos.html", datos_cliente=datos_cliente, monto_bs=monto_bs, form=form)

# TODO: Diseñar pagina de pagos
# TODO: poner verde si no tiene deuda


