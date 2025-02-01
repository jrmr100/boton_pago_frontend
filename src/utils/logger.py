import logging
from dotenv import load_dotenv
import os
from datetime import datetime


# Cargo la variable de entorno
load_dotenv()

# Configuro los parámetros y formatos del logging
now = datetime.now()
today = now.strftime('%d%m%Y')

logging.basicConfig(handlers=[logging.FileHandler(filename=os.getenv("LOG_FILE") +
                                                           os.getenv("NOMBRE_PROYECTO") +
                                                  "_" + today + ".log",
                    encoding='utf-8', mode='a+')],
                    level=int(os.getenv("LOG_LEVEL")),
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)