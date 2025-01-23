from flask import render_template, Blueprint
from src.routes.form_bp.templates.form_fields import FormFields
import logging

# Creo mi logging del modulo
logger = logging.getLogger(__name__)

nombre_ruta = "formulario"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix="/" + nombre_ruta
)


# ############MOSTRAR HOME################
@blue_ruta.route('/', methods=["GET", "POST"])
def formulario():
    form = FormFields()
    if form.validate_on_submit():
        print("Formulario enviado")

    return render_template("webpage.html", form=form)
