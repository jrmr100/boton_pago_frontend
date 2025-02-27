from dotenv import load_dotenv
import os


# Cargo las variables de entorno previo a mis modulos
app_dir = os.path.join(os.path.dirname(__file__))
load_dotenv(app_dir + "/.env")

from utils.api_vippo import buscar_tasabcv
from utils.api_vippo import buscar_listabancos



# se debe crear un crontab para q se ejecute de lun a vie cada 4hrs
# sudo crontab -e
# 0 1,5,9,13,17 * * 1-5 cd /var/www/boton_pago/src/utils && sudo -u www-data venv/bin/python3 crontab.py

# Obtener la tasa BCV desde vippo
buscar_tasabcv()

# Obtener la tasa BCV desde vippo
buscar_listabancos()


