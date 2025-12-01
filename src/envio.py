from flask import Blueprint, request
from src.db import get_db_connection

envio_bp = Blueprint("envio", __name__)

@envio_bp.route("/envio", methods=["GET", "POST"])
def registrar_envio():
    if request.method == "POST":
        factura_id = request.form.get("factura_id")
        comentario = request.form.get("comentario") or "Productos despachados."

        conn = get_db_connection()

        # DEMO Render
        if conn is None:
            return f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Envío registrado</title>
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
                        max-width: 520px;
                        width: 90%;
                        box-shadow: 0 18px 35px rgba(0,0,0,0.55);
                        border: 1px solid rgba(148,163,184,0.35);
                    }}
                    h2 {{ margin-top: 0; }}
                    p span {{ font-weight: 600; }}
                    a {{ color: #22c55e; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h2>Envío registrado (DEMO Render)</h2>
                    <p><span>ID Factura:</span> {factura_id}</p>
                    <p><span>Comentario:</span> {comentario}</p>
                    <p style="color:orange;">⚠ Registro no guardado en BD (modo demo).</p>
                    <br>
                    <a href="/menu">Volver al menú</a>
                </div>
            </body>
            </html>
            """

        # MODO LOCAL: guardar en BD
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO envios (factura_id, comentario) VALUES (%s, %s)",
            (factura_id, comentario)
        )

        # Si tienes columna estado en facturas, puedes actualizarla
        try:
            cursor.execute(
                "UPDATE facturas SET estado = %s WHERE id = %s",
                ("despachada", factura_id)
            )
        except Exception:
            pass

        conn.commit()
        cursor.close()
        conn.close()

        return """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Envío registrado</title>
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
                <h2>Envío registrado correctamente</h2>
                <p>El despacho ha sido registrado en la base de datos.</p>
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
        <title>Registrar Envío</title>
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
                max-width: 520px;
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
            <h2>Registrar Envío</h2>
            <form method="POST">
                <div class="group">
                    <label>ID de Factura</label>
                    <input name="factura_id" required>
                </div>
                <div class="group">
                    <label>Comentario</label>
                    <input name="comentario" placeholder="Productos despachados.">
                </div>

                <button type="submit">Registrar Envío</button>
            </form>
            <a href="/menu">Volver al menú</a>
        </div>
    </body>
    </html>
    """
