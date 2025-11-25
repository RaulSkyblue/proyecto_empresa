from src.login import login_bp
from src.orden_compra import orden_compra_bp
from src.factura import factura_bp
from src.envio import envio_bp


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
