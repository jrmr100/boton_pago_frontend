import sqlite3
import os
import logging
from contextlib import contextmanager

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta dinámica corregida
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'boton_pagos.db'))


@contextmanager
def get_db():
    """Context manager para asegurar que la conexión siempre se cierre y maneje transacciones."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Error de base de datos: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Inicializa la base de datos con una estructura limpia."""
    # Usamos tipos REAL para montos y TIMESTAMP para fechas por eficiencia
    sql_create_table = '''
                       CREATE TABLE IF NOT EXISTS pagos_tdc \
                       ( \
                           id \
                           INTEGER \
                           PRIMARY \
                           KEY \
                           AUTOINCREMENT, \
                           url_orden_pago \
                           TEXT \
                           NOT \
                           NULL, \
                           payment_request_id \
                           TEXT \
                           UNIQUE \
                           NOT \
                           NULL, \
                           fecha_hora \
                           TEXT \
                           NOT \
                           NULL, \
                           order_number \
                           TEXT \
                           NOT \
                           NULL, \
                           monto_bs \
                           REAL \
                           NOT \
                           NULL, \
                           created_at \
                           TIMESTAMP \
                           DEFAULT \
                           CURRENT_TIMESTAMP
                       ) \
                       '''
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_create_table)
            # El manejo de migraciones (ALTER TABLE) es mejor hacerlo por scripts separados,
            # pero para mantener tu lógica, aquí está simplificada:
            columns = [info[1] for info in cursor.execute("PRAGMA table_info(pagos_tdc)")]
            if "monto_bs" not in columns:
                cursor.execute("ALTER TABLE pagos_tdc ADD COLUMN monto_bs REAL")

            conn.commit()
            logger.info("Base de datos verificada/inicializada")
            return True
    except Exception:
        return False


def registrar_pago(url_orden_pago, payment_id, fecha_transaccion, order_number, monto_bs):
    """
    Registra un pago utilizando el context manager optimizado.
    """
    sql = '''
          INSERT INTO pagos_tdc (url_orden_pago, payment_request_id, fecha_hora, order_number, monto_bs)
          VALUES (?, ?, ?, ?, ?) \
          '''
    try:
        with get_db() as conn:
            conn.execute(sql, (url_orden_pago, payment_id, fecha_transaccion, order_number, float(monto_bs)))
            conn.commit()
            logger.info(f"Éxito: Pago {order_number} registrado en db.")
            return True
    except Exception as e:
        logger.error(f"Fallo al registrar pago {order_number}: {e}")
        return False