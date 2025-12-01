from flask import Blueprint, request
from src.db import get_db_connection

factura_bp = Blueprint("factura", __name__)

@factura_bp.route("/factura", methods=["GET", "POST"])
def generar_factura():
    if request.method == "POST":
        cliente = request.form.get("cliente")
        producto = request.form.get("producto")
        cantidad = int(request.form.get("cantidad") or 0)
        precio_unitario = float(request.form.get("precio_unitario") or 0)

        subtotal = cantidad * precio_unitario
        iva = round(subtotal * 0.19, 2)
        total = round(subtotal + iva, 2)

        conn = get_db_connection()

        # DEMO Render (sin BD)
        if conn is None:
            return f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Factura generada</title>
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
                        max-width: 560px;
                        width: 95%;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
                        border: 1px solid rgba(148,163,184,0.35);
                    }}
                    h2 {{ margin-top: 0; }}
                    p span {{ font-weight: 600; }}
                    hr {{ border: none; border-top: 1px solid rgba(148,163,184,0.4); margin: 14px 0; }}
                    a {{ color: #22c55e; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>Factura generada (DEMO Render)</h2>
                    <p><span>Cliente:</span> {cliente}</p>
                    <p><span>Producto:</span> {producto}</p>
                    <p><span>Cantidad:</span> {cantidad}</p>
                    <p><span>Precio unitario:</span> ${precio_unitario}</p>
                    <hr>
                    <p><span>Subtotal:</span> ${subtotal}</p>
                    <p><span>IVA (19%):</span> ${iva}</p>
                    <p><span>Total a pagar:</span> ${total}</p>
                    <p style="color:orange;">⚠ Factura no guardada en BD (modo demo).</p>
                    <br>
                    <a href="/menu">Volver al menú</a>
                </div>
            </body>
            </html>
            """

        # MODO LOCAL: guardar en BD
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO facturas (cliente, producto, cantidad, precio_unitario, subtotal, iva, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (cliente, producto, cantidad, precio_unitario, subtotal, iva, total)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Factura guardada</title>
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
                    max-width: 480px;
                    width: 90%;
                    text-align: center;
                    box-shadow: 0 18px 35px rgba(0,0,0,0.55);
                    border: 1px solid rgba(148,163,184,0.35);
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
                <h2>Factura guardada correctamente</h2>
                <p>La información fue almacenada en la base de datos.</p>
                <br>
                <a href="/menu">Volver al menú</a>
            </div>
        </body>
        </html>
        """

    # GET → formulario visual
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Emisión de Factura</title>
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
            <h2>Emisión de Factura</h2>
            <form method="POST">
                <div class="group">
                    <label>Cliente</label>
                    <input name="cliente" required>
                </div>
                <div class="group">
                    <label>Producto</label>
                    <input name="producto" required>
                </div>
                <div class="row">
                    <div class="group">
                        <label>Cantidad</label>
                        <input name="cantidad" type="number" min="1" required>
                    </div>
                    <div class="group">
                        <label>Precio unitario</label>
                        <input name="precio_unitario" type="number" step="0.01" min="0" required>
                    </div>
                </div>

                <button type="submit">Generar Factura</button>
            </form>
            <a href="/menu">Volver al menú</a>
        </div>
    </body>
    </html>
    """
