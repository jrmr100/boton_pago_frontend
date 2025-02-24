from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from src.utils.logger import logger
from datetime import timedelta
import os
from src.utils.api_mw import buscar_cliente


# IMPORTACIÓN DE RUTAS
from src.routes.home_bp.route import blue_ruta as home
from src.routes.pagos_bp.route import blue_ruta as pagos
from src.routes.pagomovil_bp.route import blue_ruta as pagomovil



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config['ENV'] = '.venv'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=float(os.getenv("SESSION_TIME")))
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home.home'

@login_manager.user_loader
def load_user(client_id):
    try:
        resultado_apimw = buscar_cliente(client_id)
        if resultado_apimw[0] == "success":
            if resultado_apimw[1]["estado"] == "exito":
                return resultado_apimw
            else:
                return None



csrf = CSRFProtect()
csrf.init_app(app)

# Registros de BLUEPRINT
app.register_blueprint(home)
app.register_blueprint(pagos)
app.register_blueprint(pagomovil)



logger.info("Iniciando el programa...")
if __name__ == '__main__':
    context = ('src/cert.pem', 'src/key.pem')
    app.run(debug=True, host='0.0.0.0', port=8000, ssl_context=context)