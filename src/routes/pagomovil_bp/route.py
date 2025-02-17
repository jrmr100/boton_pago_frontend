from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.pagomovil_bp.templates.form_fields import FormFields
from src.utils.api_vippo import leer_listabancos, validar_pago
from src.utils.api_mw import buscar_facturas
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
        return render_template("error_general.html", msg="Error obteniendo la lista de bancos, intente mas tarde",
                               error="No es posible acceder a la lista de bancos emisores", type="500")
    else:
        form.entity.choices = listabancos

    # Carga de los tipos de ID al selectfield ID
    form.tipo_id.choices = config.lista_id

    # Carga de los tipos de telefonos al selectfield PHONE
    form.tipo_phone.choices = config.lista_phone


    if form.enviar.data and form.validate_on_submit(): # Boton de aceptar

        id_customer = form.tipo_id.data + form.payerID.data
        phone_payer = form.tipo_phone.data[1:] + form.payerPhone.data
        entity = form.entity.data[:4]
        order = form.order.data
        montobs = session["monto_bs"]
        datos_cliente = session["datos_cliente"]

        resultado_val = validar_pago(id_customer, phone_payer, entity, order, montobs )
        logger.debug("user: " + str(datos_cliente) + "Resultado de validacion del pago: " + str(resultado_val))

        if resultado_val[0] == "success":
            if resultado_val[1]["message"] == "Operación realizada con éxito.":
                img_entity = 'img/logo_bancoplaza.png'
                img_result = 'img/exito.png'
                id_cliente = str(datos_cliente["datos"][0]["id"])


                facturas_cliente = buscar_facturas(id_cliente,
                                                   datos_cliente["datos"][0]["id"], montobs)
                resultado_apimw = facturas_cliente.buscar_facturas()
                logger.debug("user: " + str(datos_cliente) +
                             " TYPE: Respuesta MW buscando facturas: " + str(resultado_apimw))

                return render_template('pay_result.html', msg=resultado_val[1]["message"],
                                       datos_cliente=datos_cliente, img_entity=img_entity,
                                       id_customer=id_customer,
                                       phone_payer=form.tipo_phone.data + form.payerPhone.data,
                                       entity=form.entity.data[6:], order=order, monto_bs=montobs,
                                       img_result=img_result)
            else:
                img_entity = 'img/logo_bancoplaza.png'
                img_result = 'img/error.png'
                return render_template('pay_result.html', msg=resultado_val[1]["result"]["label"],
                                       datos_cliente=datos_cliente, img_entity=img_entity,
                                       id_customer=id_customer,
                                       phone_payer=form.tipo_phone.data + form.payerPhone.data,
                                       entity=form.entity.data[6:], order=order, monto_bs=montobs,
                                       img_result=img_result)
        elif resultado_val[0] == "except":
            return render_template("error_general.html", msg="Error validando el pago, intente mas tarde",
                                   error="No es posible validar el pago:" + str(resultado_val[1]), type="500")
        else:
            return render_template("error_general.html", msg="Error validando el pago, intente mas tarde",
                                   error="No es posible validar el pago:" + str(resultado_val[1]), type="500")


    elif form.regresar.data: # boton de cancelar
        return redirect(url_for('pagos.pagos'))

    else:
        return render_template('pagomovil.html', form=form, datos_cliente=datos_cliente, pm_bancoplaza=config.pm_bancoplaza, montobs=montobs )



# TODO: Revisar el token_generator en .env, se usa?

