from flask import render_template, Blueprint, session

nombre_ruta = "pagos"

# Defino el Blueprint
blue_ruta = Blueprint(
    nombre_ruta, __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/' + nombre_ruta
)


@blue_ruta.route('/' + nombre_ruta, methods=["GET", "POST"])
def pagos():


    datos_cliente = session["datos_cliente"]
    print(datos_cliente["datos"][0]["nombre"])
    return render_template("pagos.html", datos_cliente=datos_cliente)

# TODO: Diseñar pagina de pagos

