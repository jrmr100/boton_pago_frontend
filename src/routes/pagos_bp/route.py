from flask import render_template, Blueprint, session
from src.utils.api_vippo import leer_tasa_bcv
from src.utils.logger import logger


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
    # Obtengo la tasa BCV desde la funcion
    tasa_bcv = leer_tasa_bcv()
    if "error tasa_bcv" in tasa_bcv:
        logger.error("Error obteniendo la tasa BCV desde el archivo TXT: " + str(tasa_bcv) + "\n")
        return render_template("error_general.html", msg="Error obteniendo tasa BCV,"
                               " intente mas tarde", error="No es posible acceder al valor de la tasa BCV", type="500")
    else:
        logger.info("Tasa obtenida del archivo TXT: " + str(tasa_bcv))


    datos_cliente = session["datos_cliente"]
    # Calculo el monto en Bs
    montodls = datos_cliente["datos"][0]["facturacion"]["total_facturas"]
    montobs_long =  float(montodls) * float(tasa_bcv)
    monto_bs = "{:.2f}".format(montobs_long)


    return render_template("pagos.html", datos_cliente=datos_cliente, monto_bs=monto_bs)

# TODO: Diseñar pagina de pagos


