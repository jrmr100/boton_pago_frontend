from flask import Flask
from flask_login import LoginManager
from src.routes.home_bp.templates.form_fields import User
from flask_wtf import CSRFProtect
from src.utils.logger import logger
from datetime import timedelta
import os

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
    return User(user_id)

# IMPORTACIÓN DE RUTAS
from src.routes.home_bp.route import blue_ruta as home
from src.routes.pagos_bp.route import blue_ruta as pagos
from src.routes.pagomovil_bp.route import blue_ruta as pagomovil

# Registros de BLUEPRINT
app.register_blueprint(home)
app.register_blueprint(pagos)
app.register_blueprint(pagomovil)



logger.info("Iniciando el programa...")
if __name__ == '__main__':
    context = ('src/cert.pem', 'src/key.pem')
    app.run(debug=True, host='0.0.0.0', port=8000, ssl_context=context)