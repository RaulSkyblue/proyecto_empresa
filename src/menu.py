from flask import Blueprint

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu")
def menu():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Menú Principal</title>
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
                max-width: 650px;
                width: 90%;
                background: rgba(15, 23, 42, 0.95);
                border-radius: 16px;
                padding: 32px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(148, 163, 184, 0.3);
            }
            h1 {
                margin-top: 0;
                text-align: center;
                font-size: 28px;
                color: #f9fafb;
            }
            p {
                text-align: center;
                color: #cbd5e1;
            }
            .options {
                margin-top: 25px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            a.btn {
                display: block;
                padding: 14px;
                text-decoration: none;
                border-radius: 10px;
                text-align: center;
                font-size: 16px;
                font-weight: 600;
                transition: 0.2s;
                border: 1px solid rgba(148, 163, 184, 0.4);
                background: rgba(30, 41, 59, 0.8);
                color: #e2e8f0;
            }
            a.btn:hover {
                background: rgba(51, 65, 85, 0.9);
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
                transform: translateY(-1px);
            }
            a.logout {
                margin-top: 18px;
                background: #ef4444;
                border-color: rgba(255, 255, 255, 0.3);
            }
            a.logout:hover {
                background: #dc2626;
                box-shadow: 0 6px 18px rgba(239, 68, 68, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Menú Principal</h1>
            <p>Selecciona una opción para continuar</p>

            <div class="options">
                <a href="/orden" class="btn">📄 Crear Orden de Compra</a>
                <a href="/factura" class="btn">🧾 Generar Factura</a>
                <a href="/envio" class="btn">📦 Registrar Envío</a>
                <a href="/login" class="logout">Cerrar sesión</a>
            </div>
        </div>
    </body>
    </html>
    """
