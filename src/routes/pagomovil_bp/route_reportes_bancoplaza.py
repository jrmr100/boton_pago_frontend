from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.pagomovil_bp.templates.form_fields_bancos import FormFieldsBancos
from src.routes.pagomovil_bp.templates.form_fields_reportes import FormFieldsReportes


from src.utils.api_vippo import leer_listabancos, validar_pago
from src.utils.api_mw import buscar_facturas, pagar_facturas
from src.utils.logger import logger
from flask_login import login_required, current_user
import src.config as config

nombre_ruta = "pagomovil_reportes"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)

# Cargo la lista de bancos solo una vez cuando se acceda a la ruta pagomovil
listabancos = None

@blue_ruta.before_request
@login_required
def cargar_listabancos():
    global listabancos
    if listabancos is None:
        listabancos = leer_listabancos()
        # Carga de los bancos emisores al selectfield ENTITY
        if "error listabancos" in listabancos:
            return render_template("error_general.html", msg="Error obteniendo la lista de bancos, intente mas tarde",
                                   error="No es posible acceder a la lista de bancos emisores", type="500")
        else:
            return None
    else:
        return None
@blue_ruta.after_request
def add_header(response):
    """
    Evito que los navegadores metan en cache
    esta pagina y no afecte el spinner
    """
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

@blue_ruta.after_request
def add_header(response):
    """
    Evito que los navegadores metan en cache
    esta pagina y no afecte el spinner
    """
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response


@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
@login_required
def pagomovil_reportes():
    form_bancos = FormFieldsBancos()
    form_reportes = FormFieldsReportes()

    datos_cliente = current_user.datos_cliente
    montobs = session["monto_bs"]
    form_reportes.entity.choices = listabancos

    # Carga de los tipos de ID al selectfield ID
    form_reportes.tipo_id.choices = config.lista_id

    # Carga de los tipos de telefonos al selectfield PHONE
    form_reportes.tipo_phone.choices = config.lista_phone

    if form_bancos.validate_on_submit():
        if form_bancos.submit_bancoplaza.data:  # Si se presiona el boton de submit1
            return render_template('pagomovil_reporte.html',
                                   datos_cliente=datos_cliente, pm_pagomovil=config.pm_bancoplaza,
                                   form=form_reportes, montobs=montobs)

        elif form_bancos.submit_banesco.data:  # Si se presiona el boton de submit1
            return render_template('pagomovil_reporte.html', datos_cliente=datos_cliente,
                                   pm_pagomovil=config.pm_banesco, form=form_reportes, montobs=montobs)
        else:
            return None

    elif form_reportes.validate_on_submit():
        id_customer = form_reportes.tipo_id.data + form_reportes.payerID.data
        phone_payer = form_reportes.tipo_phone.data[1:] + form_reportes.payerPhone.data
        entity = form_reportes.entity.data[:4]
        order = form_reportes.order.data
        montobs = session["monto_bs"]
        datos_cliente = current_user.datos_cliente
        img_entity = 'img/logo_bancoplaza.png'
        id_cliente = str(datos_cliente["id"])
        client_id = str(datos_cliente["cedula"])

        if form_reportes.submit_reportes.data:  # Si se presiona el boton de submit1
            return render_template('pay_result.html', msg="Pago realizado con éxito",
                               img_entity=img_entity,
                               id_customer=id_customer,
                               phone_payer=form_reportes.tipo_phone.data + form_reportes.payerPhone.data,
                               entity=form_reportes.entity.data[6:], order=order, monto_bs=0,
                               img_result=form_reportes, datos_cliente=datos_cliente)
        return None

    else:
            return render_template('pagomovil_reporte.html', form=form_reportes, datos_cliente=datos_cliente,
                               pm_pagomovil=config.pm_bancoplaza,
                               montobs=montobs)
