from flask import render_template, Blueprint, session
from src.routes.pagomovil_bp.templates.form_fields import FormFields
from src.utils.api_vippo import leer_listabancos
from src.utils.logger import logger
import src.config as config
import os



nombre_ruta = "pagomovil"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)

@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
def pagomovil():
    form = FormFields()
    datos_cliente = session["datos_cliente"]
    montobs = session["monto_bs"]


    if form.validate_on_submit():
        print("AAAA")

    else:
        # Carga la lista de bancos desde el archivo TXT
        listabancos = leer_listabancos()
        if "error listabancos" in listabancos:
            logger.error("Error obteniendo la lista de bancos desde el archivo TXT: " + str(listabancos) + "\n")
            return render_template("error_general.html", msg="Error obteniendo la lista de bancos, intente mas tarde",
                                   error="No es posible acceder a la lista de bancos emisores", type="500")
        else:
            logger.info("Lista banco obtenida del archivo TXT: " + str(listabancos))
            form.entity.choices = listabancos

        # Carga de los tipos de ID al selectfield ID
        form.tipo_id.choices = config.lista_id

        # Carga de los tipos de telefonos al selectfield PHONE
        form.tipo_phone.choices = config.lista_phone

        return render_template('pagomovil.html', form=form, datos_cliente=datos_cliente, pm_bancoplaza=config.pm_bancoplaza, montobs=montobs )





