from flask import Blueprint, request
from src.db import get_db_connection

envio_bp = Blueprint("envio", __name__)

@envio_bp.route("/envio", methods=["GET", "POST"])
def registrar_envio():
    """
    RF5: Envío de productos
    - Seleccionar factura por ID
    - Marcar productos como despachados
    - Agregar texto indicativo en la base de datos
    """

    if request.method == "POST":
        factura_id = request.form.get("factura_id")
        comentario = request.form.get("comentario") or "Productos despachados."

        conn = get_db_connection()

        # MODO DEMO (Render sin BD)
        if conn is None:
            return f"""
            <h2>Envío registrado (DEMO Render)</h2>
            <p><b>Factura ID:</b> {factura_id}</p>
            <p><b>Comentario:</b> {comentario}</p>
            <p style="color:orange;">⚠ Este registro es solo demostrativo. No se guardó en base de datos.</p>
            <br>
            <a href="/envios">Ver listado de envíos (si aplica)</a><br>
            <a href="/menu">Volver al menú</a>
            """

        # MODO LOCAL (MySQL)
        cursor = conn.cursor()

        # Opcional: actualizar estado de la factura (si tienes campo estado)
        try:
            # Ejemplo: tabla envios con factura_id y comentario
            cursor.execute(
                """
                INSERT INTO envios (factura_id, comentario)
                VALUES (%s, %s)
                """,
                (factura_id, comentario)
            )

            # Si tu tabla facturas tiene un campo "estado", puedes actualizarlo:
            try:
                cursor.execute(
                    "UPDATE facturas SET estado = %s WHERE id = %s",
                    ("despachada", factura_id)
                )
            except Exception:
                # Si no existe el campo estado, ignoramos este paso
                pass

            conn.commit()
        finally:
            cursor.close()
            conn.close()

        return f"""
        <h2>Envío registrado correctamente</h2>
        <p><b>Factura ID:</b> {factura_id}</p>
        <p><b>Comentario:</b> {comentario}</p>
        <br>
        <a href="/envios">Ver listado de envíos</a><br>
        <a href="/menu">Volver al menú</a>
        """

    # GET → mostrar formulario
    return """
    <h2>Registrar Envío</h2>
    <form method="POST">
        ID de Factura: <input name="factura_id" required><br><br>
        Comentario: <input name="comentario" placeholder="Productos despachados."><br><br>
        <button type="submit">Registrar Envío</button>
    </form>
    <br>
    <a href="/envios">Ver listado de envíos</a><br>
    <a href="/menu">Volver al menú</a>
    """


@envio_bp.route("/envios")
def listar_envios():
    """
    Listado de envíos registrados.
    """

    conn = get_db_connection()

    if conn is None:
        # DEMO EN RENDER
        return """
        <h2>Listado de Envíos (DEMO Render)</h2>
        <table border="1" cellpadding="5">
            <tr>
                <th>ID</th>
                <th>ID Factura</th>
                <th>Comentario</th>
            </tr>
            <tr>
                <td>1</td>
                <td>101</td>
                <td>Productos despachados (ejemplo demo).</td>
            </tr>
        </table>
        <p style="color:orange;">⚠ BD desactivada en Render. Datos solo demostrativos.</p>
        <br>
        <a href="/envio">Registrar nuevo envío</a><br>
        <a href="/menu">Volver al menú</a>
        """

    # MODO LOCAL: leer desde la tabla envios
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, factura_id, comentario FROM envios ORDER BY id DESC")
    envios = cursor.fetchall()
    cursor.close()
    conn.close()

    # Construir tabla HTML
    html = """
    <h2>Listado de Envíos</h2>
    <table border="1" cellpadding="5">
        <tr>
            <th>ID</th>
            <th>ID Factura</th>
            <th>Comentario</th>
        </tr>
    """

    for e in envios:
        html += f"""
        <tr>
            <td>{e["id"]}</td>
            <td>{e["factura_id"]}</td>
            <td>{e["comentario"]}</td>
        </tr>
        """

    html += """
    </table>
    <br>
    <a href="/envio">Registrar nuevo envío</a><br>
    <a href="/menu">Volver al menú</a>
    """

    return html
