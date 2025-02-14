from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.pagomovil_bp.templates.form_fields import FormFields
from src.utils.api_vippo import leer_listabancos, validar_pago
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


    if form.enviar.data and form.validate_on_submit():
        id_customer = form.tipo_id.data + form.payerID.data
        phone_payer = form.tipo_phone.data[1:] + form.payerPhone.data
        entity = form.entity.data[:4]
        order = form.order.data
        montobs = session["monto_bs"]
        datos_cliente = session["datos_cliente"]


        resultado_val = validar_pago(id_customer, phone_payer, entity, order, montobs )
        logger.debug("user: " + str(datos_cliente) + "Resultado de validacion del pago: " + str(resultado_val))
        return render_template('pay_result.html')
    elif form.regresar.data:
        return redirect(url_for('pagos.pagos'))

    else:
        return render_template('pagomovil.html', form=form, datos_cliente=datos_cliente, pm_bancoplaza=config.pm_bancoplaza, montobs=montobs )





