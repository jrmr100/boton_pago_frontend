from src.utils.logger import logger
from src.utils.api_vippo import buscar_tasabcv
from src.utils.api_vippo import buscar_listabancos


from dotenv import load_dotenv

load_dotenv()

# se debe crear un crontab para q se ejecute de lun a vie cada 4hrs
# sudo crontab -e
# 0 1,5,9,13,17 * * 1-5 cd /var/www/boton_pago/src/utils && sudo -u www-data venv/bin/python3 crontab.py

# Obtener la tasa BCV desde vippo
buscar_tasabcv()

# Obtener la tasa BCV desde vippo
buscar_listabancos()


