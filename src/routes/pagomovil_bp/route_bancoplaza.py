from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.pagomovil_bp.templates.form_fields_reportes import FormFieldsReportes

from src.utils.api_vippo import leer_listabancos
from src.utils.logger import logger
from flask_login import login_required, current_user
import src.config as config

nombre_ruta = "pagomovil_bancoplaza"

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
def pagomovil_bancoplaza():
    form_reportes = FormFieldsReportes()
    datos_cliente = current_user.datos_cliente
    montobs = session["monto_bs"]
    form_reportes.entity.choices = listabancos

    # Carga de los tipos de ID al selectfield ID
    form_reportes.tipo_id.choices = config.lista_id

    # Carga de los tipos de telefonos al selectfield PHONE
    form_reportes.tipo_phone.choices = config.lista_phone

    if form_reportes.validate_on_submit():
        return render_template('pagomovil_reportes.html', form=form_reportes, datos_cliente=datos_cliente,
                           pm_pagomovil=config.pm_bancoplaza,
                           montobs=montobs)

    else:
        return render_template('pagomovil_reportes.html', form=form_reportes, datos_cliente=datos_cliente,
                           pm_pagomovil=config.pm_bancoplaza,
                           montobs=montobs)
