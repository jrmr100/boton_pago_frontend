from flask import render_template, Blueprint

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


    return render_template("pagomovil.html")

