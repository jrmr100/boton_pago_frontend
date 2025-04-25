from flask import  Blueprint,  jsonify
from flask_login import login_required, current_user
from src.utils.api_instapago import generar_qr



nombre_ruta = "generarqr"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
@login_required
def generarqr(url_param):
    qr_image = generar_qr()
    return jsonify({"qr_image": qr_image})
