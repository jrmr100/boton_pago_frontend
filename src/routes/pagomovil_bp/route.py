from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.pagomovil_bp.templates.form_fields import FormFields
from src.utils.api_vippo import leer_listabancos, validar_pago
from src.utils.api_mw import buscar_facturas, pagar_facturas
from src.utils.logger import logger
from flask_login import login_required, current_user
import src.config as config

nombre_ruta = "pagomovil_bancos"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
@login_required
def pagomovil_bancos():
    form = FormFields()
    datos_cliente = current_user.datos_cliente
    montobs = session["monto_bs"]

    if form.validate_on_submit():
        return render_template('pagomovil.html',  datos_cliente=datos_cliente)

    else:
        return render_template('pagomovil.html', form=form, datos_cliente=datos_cliente,
                               pm_bancoplaza=config.pm_bancoplaza,
                               pm_banesco=config.pm_banesco,
                               montobs=montobs)