from flask import Blueprint, request
from src.db import get_db_connection

orden_compra_bp = Blueprint('orden_compra', __name__)

@orden_compra_bp.route('/orden', methods=['GET', 'POST'])
def crear_orden():
    if request.method == 'POST':
        cliente = request.form.get('cliente')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        comuna = request.form.get('comuna')
        region = request.form.get('region')
        producto = request.form.get('producto')
        precio = float(request.form.get('precio') or 0)

        conn = get_db_connection()

        # MODO DEMO (Render sin BD)
        if conn is None:
            return f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Orden registrada</title>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: Arial, Helvetica, sans-serif;
                        background: linear-gradient(135deg, #1e293b, #0f172a);
                        color: #e5e7eb;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                    }}
                    .card {{
                        background: rgba(15,23,42,0.96);
                        border-radius: 18px;
                        padding: 28px 30px;
                        max-width: 600px;
                        width: 90%;
                        box-shadow: 0 18px 35px rgba(0,0,0,0.55);
                        border: 1px solid rgba(148,163,184,0.35);
                    }}
                    h2 {{
                        margin-top: 0;
                        color: #f9fafb;
                    }}
                    p span {{
                        font-weight: 600;
                    }}
                    a {{
                        color: #22c55e;
                        text-decoration: none;
                        font-weight: 600;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>Orden de compra registrada (DEMO Render)</h2>
                    <p><span>Cliente:</span> {cliente}</p>
                    <p><span>Dirección:</span> {direccion}</p>
                    <p><span>Teléfono:</span> {telefono}</p>
                    <p><span>Comuna:</span> {comuna}</p>
                    <p><span>Región:</span> {region}</p>
                    <p><span>Producto:</span> {producto}</p>
                    <p><span>Precio:</span> ${precio}</p>
                    <p style="color:orange;">⚠ Datos no guardados en BD (modo demo).</p>
                    <br>
                    <a href="/menu">Volver al menú</a>
                </div>
            </body>
            </html>
            """

        # MODO LOCAL (con BD)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO ordenes 
                (cliente, direccion, telefono, comuna, region, producto, precio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (cliente, direccion, telefono, comuna, region, producto, precio)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Orden registrada</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: Arial, Helvetica, sans-serif;
                    background: linear-gradient(135deg, #1e293b, #0f172a);
                    color: #e5e7eb;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }}
                .card {{
                    background: rgba(15,23,42,0.96);
                    border-radius: 18px;
                    padding: 28px 30px;
                    max-width: 500px;
                    width: 90%;
                    box-shadow: 0 18px 35px rgba(0,0,0,0.55);
                    border: 1px solid rgba(148,163,184,0.35);
                    text-align: center;
                }}
                h2 {{ margin-top: 0; }}
                a {{
                    color: #22c55e;
                    text-decoration: none;
                    font-weight: 600;
                }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Orden de compra guardada correctamente</h2>
                <p>Los datos quedaron almacenados en la base de datos.</p>
                <br>
                <a href="/menu">Volver al menú</a>
            </div>
        </body>
        </html>
        """

    # GET → Formulario bonito
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Ingreso de Orden de Compra</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, Helvetica, sans-serif;
                background: linear-gradient(135deg, #1e293b, #0f172a);
                color: #e5e7eb;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .card {
                background: rgba(15,23,42,0.96);
                border-radius: 18px;
                padding: 28px 30px;
                max-width: 620px;
                width: 95%;
                box-shadow: 0 20px 40px rgba(0,0,0,0.65);
                border: 1px solid rgba(148,163,184,0.35);
            }
            h2 {
                margin-top: 0;
                font-size: 24px;
            }
            .group {
                margin-bottom: 12px;
            }
            label {
                display: block;
                font-size: 13px;
                color: #cbd5e1;
                margin-bottom: 4px;
            }
            input {
                width: 100%;
                padding: 8px 10px;
                border-radius: 8px;
                border: 1px solid rgba(148,163,184,0.4);
                background: #020617;
                color: #e5e7eb;
                font-size: 14px;
            }
            input:focus {
                outline: none;
                border-color: #22c55e;
                box-shadow: 0 0 0 1px #22c55e;
            }
            .row {
                display: flex;
                gap: 12px;
            }
            .row .group {
                flex: 1;
            }
            button {
                margin-top: 10px;
                padding: 10px 18px;
                border-radius: 999px;
                border: none;
                background: #22c55e;
                color: #022c22;
                font-weight: 600;
                cursor: pointer;
                font-size: 14px;
                box-shadow: 0 10px 22px rgba(34,197,94,0.45);
                transition: 0.15s;
            }
            button:hover {
                background: #16a34a;
                transform: translateY(-1px);
            }
            a {
                display: inline-block;
                margin-top: 14px;
                color: #e5e7eb;
                font-size: 13px;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Ingreso de Orden de Compra</h2>
            <form method="POST">
                <div class="group">
                    <label>Cliente</label>
                    <input name="cliente" required>
                </div>
                <div class="group">
                    <label>Dirección</label>
                    <input name="direccion" required>
                </div>

                <div class="row">
                    <div class="group">
                        <label>Teléfono</label>
                        <input name="telefono">
                    </div>
                    <div class="group">
                        <label>Comuna</label>
                        <input name="comuna">
                    </div>
                    <div class="group">
                        <label>Región</label>
                        <input name="region">
                    </div>
                </div>

                <div class="row">
                    <div class="group">
                        <label>Producto</label>
                        <input name="producto" required>
                    </div>
                    <div class="group">
                        <label>Precio</label>
                        <input name="precio" type="number" step="0.01" min="0" required>
                    </div>
                </div>

                <button type="submit">Registrar Orden</button>
            </form>
            <a href="/menu">Volver al menú</a>
        </div>
    </body>
    </html>
    """
