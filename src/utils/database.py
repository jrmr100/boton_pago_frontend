import sqlite3
import os
from datetime import datetime
import logging

# Simple logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'boton_pagos.db')

def get_db_connection():
    """Establece conexión con la base de datos SQLite"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error conectando a la base de datos: {e}")
        return None

def init_database():
    """Inicializa la base de datos y crea la tabla si no existe"""
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos_tdc (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_orden_pago TEXT NOT NULL,
                payment_request_id TEXT NOT NULL,
                fecha_hora TEXT NOT NULL,
                order_number TEXT NOT NULL,
                monto_bs TEXT NOT NULL,
                created_at TEXT
            )
        ''')
        
        # Add monto_bs column if it doesn't exist (for existing tables)
        try:
            cursor.execute("ALTER TABLE pagos_tdc ADD COLUMN monto_bs TEXT")
        except sqlite3.OperationalError as e:
            # Column already exists, which is fine
            if "duplicate column name" in str(e).lower():
                pass
            else:
                raise e
        
        # Ensure created_at column is TEXT type (for existing tables)
        try:
            cursor.execute("ALTER TABLE pagos_tdc ADD COLUMN created_at_new TEXT")
            cursor.execute("UPDATE pagos_tdc SET created_at_new = created_at WHERE created_at_new IS NULL")
            cursor.execute("ALTER TABLE pagos_tdc DROP COLUMN created_at")
            cursor.execute("ALTER TABLE pagos_tdc RENAME COLUMN created_at_new TO created_at")
        except sqlite3.OperationalError:
            # Column already exists or table structure is correct
            pass
        
        conn.commit()
        logger.info("Base de datos inicializada correctamente")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error inicializando la base de datos: {e}")
        return False
    finally:
        conn.close()

def pagos_db(url_orden_pago, payment_request_id, fecha_hora, order_number, monto_bs):
    """
    Almacena los datos del pago en la base de datos SQLite
    
    Args:
        url_orden_pago (str): URL de la orden de pago
        payment_request_id (str): ID del request de pago
        fecha_hora (str): Fecha y hora de la transacción
        order_number (str): Número de orden
        monto_bs (str): Monto en bolívares
    
    Returns:
        bool: True si se guardó correctamente, False si hubo error
    """
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO pagos_tdc (url_orden_pago, payment_request_id, fecha_hora, order_number, monto_bs, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (url_orden_pago, payment_request_id, fecha_hora, order_number, monto_bs, created_at))
        
        conn.commit()
        logger.info(f"Pago guardado en BD - Order: {order_number}, PaymentID: {payment_request_id}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error guardando pago en BD: {e}")
        return False
    finally:
        conn.close()
