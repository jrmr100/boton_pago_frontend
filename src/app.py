from flask import Flask, session
from flask_login import LoginManager
from src.routes.home_bp.templates.form_fields import User
from flask_wtf import CSRFProtect
from datetime import timedelta
from dotenv import load_dotenv
import os

# Cargo las variables de entorno previo a mis modulos
app_dir = os.path.join(os.path.dirname(__file__))
load_dotenv(app_dir + "/.env")

from src.utils.logger import logger
logger.info("Iniciando aplicacion en app\n")
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config['ENV'] = '.venv'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=float(os.getenv("SESSION_TIME")))

csrf = CSRFProtect()
csrf.init_app(app)

########## FLASK-LOGIN ##############
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home.home'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, session.get('datos_cliente'))

# IMPORTACIÓN DE RUTAS
from src.routes.home_bp.route import blue_ruta as home
from src.routes.pagos_bp.route import blue_ruta as pagos
from src.routes.pagomovil_bp.route_bancos import blue_ruta as pagomovil_bancos
from src.routes.pagomovil_bp.route_reportes_bancoplaza import blue_ruta as pagomovil_reportes

# Registros de BLUEPRINT
app.register_blueprint(home)
app.register_blueprint(pagos)
app.register_blueprint(pagomovil_bancos)
app.register_blueprint(pagomovil_reportes)


if __name__ == '__main__':
    context = ('src/cert.pem', 'src/key.pem')
    app.run(debug=True, host='0.0.0.0', port=8000, ssl_context=context)