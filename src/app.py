from flask import Flask
from flask_wtf import CSRFProtect
from src.utils.logger import logger
import os


# IMPORTACIÓN DE RUTAS
from src.routes.home_bp.route import blue_ruta as home
from src.routes.pagos_bp.route import blue_ruta as pagos
from src.routes.zelle_bp.route import blue_ruta as zelle
from src.routes.pagomovil_bp.route import blue_ruta as pagomovil



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
csrf = CSRFProtect()
csrf.init_app(app)

# Registros de BLUEPRINT
app.register_blueprint(home)
app.register_blueprint(pagos)
app.register_blueprint(zelle)
app.register_blueprint(pagomovil)



logger.info("Iniciando el programa...")
if __name__ == '__main__':
    context = ('src/cert.pem', 'src/key.pem')
    app.run(debug=True, host='0.0.0.0', port=8000, ssl_context=context)