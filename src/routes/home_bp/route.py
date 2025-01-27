from flask import render_template, Blueprint
from src.routes.home_bp.templates.form_fields import FormFields
import src.config as config
import logging

# Creo mi logging del modulo
logger = logging.getLogger(__name__)

nombre_ruta = "home"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/'
)


# ############MOSTRAR HOME################
@blue_ruta.route('/', methods=["GET", "POST"])
def home():
    form = FormFields()
    if form.validate_on_submit():
        print("Adentro del submit")
    # else:
        #print(form.errors)

    # Carga de los tipos CI/RIF
    form.field2.choices = config.lista_id

    return render_template("webpage.html", form=form)
