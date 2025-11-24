# src/db.py
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",          # Cambia si tu Laragon tiene clave
    "database": "proyecto_empresa"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
