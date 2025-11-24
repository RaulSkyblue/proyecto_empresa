from flask import Flask
from login import login_bp
from menu import menu_bp
from orden_compra import orden_bp
from factura import factura_bp
from envio import envio_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_clave"

    app.register_blueprint(login_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(orden_bp)
    app.register_blueprint(factura_bp)
    app.register_blueprint(envio_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
