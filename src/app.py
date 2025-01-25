from flask import Flask
from flask_wtf import CSRFProtect
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

# IMPORTACIÓN DE RUTAS
from src.routes.home_bp.route import blue_ruta as home



# Cargo la variable de entorno
load_dotenv()

# Configuro los parámetros y formatos del logging
now = datetime.now()
today = now.strftime('%d%m%Y')
# Configuro los parámetros y formatos del logging
logging.basicConfig(handlers=[logging.FileHandler(filename=os.getenv("LOG_FILE") +
                                                           os.getenv("NOMBRE_PROYECTO") +
                                                  "-" + today + ".log",
                    encoding='utf-8', mode='a+')],
                    level=int(os.getenv("LOG_LEVEL")),
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
csrf = CSRFProtect()
csrf.init_app(app)

# Registros de BLUEPRINT
app.register_blueprint(home)


logger.info("Iniciando el programa...")
if __name__ == '__main__':
    context = ('src/cert.pem', 'src/key.pem')
    app.run(debug=True, host='0.0.0.0', port=8000, ssl_context=context)