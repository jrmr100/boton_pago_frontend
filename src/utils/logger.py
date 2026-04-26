import logging
import os
from datetime import datetime

# --- Configuración Base ---
project_name = os.getenv("NOMBRE_PROYECTO", "app")
log_level_env = os.getenv("LOG_LEVEL", "20")  # default INFO=20
is_production = os.getenv("IS_PRODUCTION")  # Variable clave para la decisión

now = datetime.now()

try:
    log_level = int(log_level_env)
except ValueError:
    log_level = getattr(logging, log_level_env.upper(), logging.INFO)

logger = logging.getLogger(project_name)
logger.setLevel(log_level)

# Formato general de logs
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

# --- 1. Handler a STDOUT/STDERR (Para Systemd/Journalctl) ---
# Este handler se mantiene SIEMPRE, ya que Systemd lo captura en producción.
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# --- 2. Handler de Archivo (Condicional para Entornos No-Prod) ---
if not is_production:
    print(f"Modo de desarrollo/local detectado. Se crearán logs en archivos.")

    # Lógica de archivo (originalmente tuya)
    today = datetime.now().strftime('%d%m%Y')
    folder_base = os.getenv("LOG_FILE", "log/")
    os.makedirs(folder_base, exist_ok=True)
    log_path = os.path.join(folder_base, f"{project_name}_{today}.log")

    file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="a")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Evitar propagación a root logger
logger.propagate = False