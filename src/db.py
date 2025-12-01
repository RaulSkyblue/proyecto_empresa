import os
import mysql.connector
from mysql.connector import Error

# Detectar si estamos en Render (variable de entorno)
IS_RENDER = os.getenv("RENDER", "0") == "1"

# Configuración de BD para uso LOCAL (Laragon)
LOCAL_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "proyecto_empresa"
}


def get_connection():
    """
    Retorna la conexión a la base de datos.

    - En Render (IS_RENDER = True): devuelve None para evitar fallos,
      porque la BD local de Laragon no existe en la nube.
    - En local: intenta conectarse a MySQL usando LOCAL_DB_CONFIG.
    """

    if IS_RENDER:
        # Modo demo en Render: no conectamos a MySQL
        print("⚠ BD DESACTIVADA EN RENDER (modo demo, sin conexión a MySQL).")
        return None

    # Modo local (Laragon)
    try:
        conn = mysql.connector.connect(**LOCAL_DB_CONFIG)
        return conn
    except Error as e:
        print(f"❌ Error conectando a MySQL local: {e}")
        return None


# 👈 ESTE ALIAS ES CLAVE PARA QUE NO FALLE
def get_db_connection():
    return get_connection()
