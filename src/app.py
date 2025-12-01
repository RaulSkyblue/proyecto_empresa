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

    # Ruta raíz "/" → página bonita
    @app.route("/")
    def index():
        return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Proyecto Empresa - Inicio</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    font-family: Arial, Helvetica, sans-serif;
                    background: linear-gradient(135deg, #1e293b, #0f172a);
                    color: #e5e7eb;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                }
                .container {
                    max-width: 800px;
                    width: 90%;
                    background: rgba(15, 23, 42, 0.95);
                    border-radius: 16px;
                    padding: 32px 28px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
                    border: 1px solid rgba(148, 163, 184, 0.3);
                }
                h1 {
                    margin-top: 0;
                    font-size: 28px;
                    color: #f9fafb;
                }
                h2 {
                    margin-top: 8px;
                    font-size: 18px;
                    font-weight: normal;
                    color: #9ca3af;
                }
                p {
                    line-height: 1.5;
                    margin-bottom: 16px;
                }
                .tags {
                    margin: 16px 0;
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }
                .tag {
                    font-size: 12px;
                    padding: 4px 10px;
                    border-radius: 999px;
                    background: rgba(51, 65, 85, 0.8);
                    border: 1px solid rgba(148, 163, 184, 0.4);
                }
                .buttons {
                    margin-top: 20px;
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                }
                a.btn {
                    text-decoration: none;
                    padding: 10px 18px;
                    border-radius: 999px;
                    font-size: 14px;
                    font-weight: 600;
                    display: inline-block;
                    transition: background 0.2s, transform 0.1s, box-shadow 0.1s;
                }
                a.btn-primary {
                    background: #22c55e;
                    color: #022c22;
                    box-shadow: 0 10px 20px rgba(34, 197, 94, 0.35);
                }
                a.btn-primary:hover {
                    background: #16a34a;
                    transform: translateY(-1px);
                    box-shadow: 0 14px 26px rgba(34, 197, 94, 0.45);
                }
                a.btn-secondary {
                    background: transparent;
                    color: #e5e7eb;
                    border: 1px solid rgba(148, 163, 184, 0.7);
                }
                a.btn-secondary:hover {
                    background: rgba(31, 41, 55, 0.9);
                }
                .footer {
                    margin-top: 22px;
                    font-size: 12px;
                    color: #9ca3af;
                    opacity: 0.9;
                }
                .footer span {
                    color: #22c55e;
                    font-weight: 600;
                }
                ul {
                    padding-left: 18px;
                    margin-top: 8px;
                    margin-bottom: 12px;
                    font-size: 14px;
                    color: #d1d5db;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Proyecto Empresa - Sistema de Gestión</h1>
                <h2>Evaluación 3 · Backend Flask + MySQL · Deploy en Render</h2>

                <p>
                    Este sistema permite gestionar el flujo básico de una empresa: 
                    autenticación de usuarios, órdenes de compra, facturación con IVA (19%)
                    y gestión de envíos. El backend está desarrollado en Python (Flask) y
                    se conecta a una base de datos MySQL en entorno local.
                </p>

                <div class="tags">
                    <div class="tag">Flask</div>
                    <div class="tag">MySQL / Laragon</div>
                    <div class="tag">Render</div>
                    <div class="tag">CI/CD con GitHub Actions</div>
                    <div class="tag">Rutas REST simples</div>
                </div>

                <p>Accesos principales del sistema:</p>
                <ul>
                    <li><b>Login</b> de usuario.</li>
                    <li><b>Órdenes de compra</b> creadas desde un formulario.</li>
                    <li><b>Facturas</b> con cálculo automático de IVA (19%) y total.</li>
                    <li><b>Envíos</b> con estado (pendiente, en tránsito, entregado).</li>
                </ul>

                <div class="buttons">
                    <a href="/login" class="btn btn-primary">Iniciar sesión</a>
                    <a href="/menu" class="btn btn-secondary">Ir al menú principal</a>
                </div>

                <div class="footer">
                    Backend ejecutándose en <span>Render</span>. En entorno local,
                    el sistema se integra con MySQL mediante Laragon.
                </div>
            </div>
        </body>
        </html>
        """

    return app


# Objeto global que usa gunicorn en Render: src.app:app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
