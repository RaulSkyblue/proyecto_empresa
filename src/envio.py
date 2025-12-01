from flask import Blueprint, request
from src.db import get_db_connection

envio_bp = Blueprint("envio", __name__)

@envio_bp.route("/envios")
def listar_envios():
    """
    Lista de envíos registrados.
    - En local: datos reales desde MySQL.
    - En Render: datos demo (sin BD).
    """

    conn = get_db_connection()
    if conn is None:
        # MODO DEMO (Render)
        return """
        <h2>Listado de Envíos (Demo Render)</h2>
        <table border="1" cellpadding="5">
            <tr>
                <th>ID</th>
                <th>Cliente</th>
                <th>Dirección</th>
                <th>Estado</th>
            </tr>
            <tr>
                <td>1</td>
                <td>Cliente Demo</td>
                <td>Calle Falsa 123</td>
                <td>En tránsito</td>
            </tr>
        </table>
        <p>⚠ BD desactivada en Render (modo demo, sin datos reales).</p>
        <p><a href="/envios/nuevo">Registrar nuevo envío</a></p>
        <p><a href="/menu">Volver al menú</a></p>
        """

    # MODO LOCAL (MySQL)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM envios ORDER BY id DESC")
    envios = cursor.fetchall()
    cursor.close()
    conn.close()

    html = """
    <h2>Listado de Envíos</h2>
    <table border="1" cellpadding="5">
        <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Dirección</th>
            <th>Estado</th>
        </tr>
    """

    for e in envios:
        html += f"""
        <tr>
            <td>{e['id']}</td>
            <td>{e['cliente']}</td>
            <td>{e['direccion']}</td>
            <td>{e['estado']}</td>
        </tr>
        """

    html += """
    </table>
    <p><a href="/envios/nuevo">Registrar nuevo envío</a></p>
    <p><a href="/menu">Volver al menú</a></p>
    """

    return html


@envio_bp.route("/envios/nuevo", methods=["GET", "POST"])
def nuevo_envio():
    """
    Registra un nuevo envío.
    - En local: inserta en MySQL.
    - En Render: muestra datos demo sin guardar.
    """

    if request.method == "POST":
        cliente = request.form.get("cliente")
        direccion = request.form.get("direccion")
        estado = request.form.get("estado")

        conn = get_db_connection()
        if conn is None:
            # MODO DEMO (Render)
            return f"""
            <h2>Envío Registrado (Demo Render)</h2>
            <p><b>Cliente:</b> {cliente}</p>
            <p><b>Dirección:</b> {direccion}</p>
            <p><b>Estado:</b> {estado}</p>
            <p>⚠ BD desactivada en Render — no se guardó en base de datos.</p>
            <p><a href="/envios">Volver al listado (demo)</a></p>
            <p><a href="/menu">Volver al menú</a></p>
            """

        # MODO LOCAL (MySQL)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO envios (cliente, direccion, estado)
            VALUES (%s, %s, %s)
            """,
            (cliente, direccion, estado)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return """
        <h2>Envío registrado correctamente.</h2>
        <p><a href="/envios">Ver lista de envíos</a></p>
        <p><a href="/menu">Volver al menú</a></p>
        """

    # GET → formulario
    return """
    <h2>Registrar Nuevo Envío</h2>
    <form method="POST">
        Cliente: <input name="cliente" required><br><br>
        Dirección: <input name="direccion" required><br><br>
        Estado:
        <select name="estado" required>
            <option value="Pendiente">Pendiente</option>
            <option value="En tránsito">En tránsito</option>
            <option value="Entregado">Entregado</option>
        </select>
        <br><br>
        <button type="submit">Registrar Envío</button>
    </form>
    <p><a href="/envios">Volver al listado</a></p>
    <p><a href="/menu">Volver al menú</a></p>
    """
