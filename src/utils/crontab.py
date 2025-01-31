import logging
import datetime
from dotenv import load_dotenv
from src.utils.api_vippo import ApiVippo
import os


load_dotenv()
logger = logging.getLogger(__name__)

# Obtener la tasa BCV desde vippo
tasa_bcv = ApiVippo().buscar_tasabcv()
print(tasa_bcv)

