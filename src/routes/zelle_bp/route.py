from flask import render_template, Blueprint, session

nombre_ruta = "zelle"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)

@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
def zelle():
    datos_cliente = session["datos_cliente"]



    return render_template("zelle.html", datos_cliente=datos_cliente)

