import logging
from datetime import datetime
import os

# Configuro los parámetros y formatos del logging
now = datetime.now()
today = now.strftime('%d%m%Y')
logging.basicConfig(handlers=[logging.FileHandler(filename=os.getenv("PATH_BASE") + os.getenv("LOG_FILE") + os.getenv("NOMBRE_PROYECTO") + "_" + today + ".log",
                    encoding='utf-8', mode='a+')],
                    level=int(os.getenv("LOG_LEVEL")),
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)