import os
import sys

# === FIX para que src sea importable tanto en local como en Render ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask
from src.login import login_bp
from src.menu import menu_bp
from src.orden_compra import orden_compra_bp
from src.factura import factura_bp
from src.envio import envio_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = "super_clave"

    # Registrar blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(orden_compra_bp)
    app.register_blueprint(factura_bp)
    app.register_blueprint(envio_bp)

    return app


# 👇 ESTA LÍNEA ES CLAVE PARA RENDER:
# Render (gunicorn) usa este objeto "app"
app = create_app()


if __name__ == "__main__":
    # Ejecución local
    app.run(debug=True)
