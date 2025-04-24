from flask import render_template, Blueprint, session, redirect, url_for
from src.routes.pagomovil_bp.templates.form_fields_bancos import FormFieldsBancos

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
    form_bancos = FormFieldsBancos()
    datos_cliente = current_user.datos_cliente
    montobs = session["monto_bs"]


    if form_bancos.validate_on_submit():
        if form_bancos.submit_bancoplaza.data:
            return redirect(url_for('pagomovil_bancoplaza.pagomovil_bancoplaza'))

        elif form_bancos.submit_banesco.data:
            return redirect(url_for('pagomovil_banesco.pagomovil_banesco'))

        else:
            return None
    else:
            return render_template('pagomovil_bancos.html', form=form_bancos, datos_cliente=datos_cliente,
                               pm_bancoplaza=config.pm_bancoplaza,
                               pm_banesco=config.pm_banesco,
                               montobs=montobs)
