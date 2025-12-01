from flask import Blueprint, request
from src.db import get_db_connection

factura_bp = Blueprint("factura", __name__)

@factura_bp.route("/factura", methods=["GET", "POST"])
def generar_factura():
    if request.method == "POST":
        cliente = request.form.get("cliente")
        producto = request.form.get("producto")
        cantidad = int(request.form.get("cantidad"))
        precio_unitario = float(request.form.get("precio_unitario"))

        subtotal = cantidad * precio_unitario
        iva = subtotal * 0.19
        total = subtotal + iva

        # Intentar conexión a BD
        conn = get_db_connection()

        # Si la conexión falla → Modo DEMO Render
        if conn is None:
            return f"""
                <h3>Factura generada (DEMO Render)</h3>
                <p><b>Cliente:</b> {cliente}</p>
                <p><b>Producto:</b> {producto}</p>
                <p><b>Cantidad:</b> {cantidad}</p>
                <p><b>Precio Unitario:</b> {precio_unitario}</p>
                <hr>
                <p><b>Subtotal:</b> ${subtotal}</p>
                <p><b>IVA (19%):</b> ${iva}</p>
                <p><b>Total a pagar:</b> ${total}</p>
                <p style="color:red;">⚠ Factura NO guardada en BD (modo demo).</p>
                <br>
                <a href="/menu">Volver al menú</a>
            """

        # Modo LOCAL (Laragon + MySQL)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO facturas (cliente, producto, cantidad, precio_unitario, subtotal, iva, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (cliente, producto, cantidad, precio_unitario, subtotal, iva, total))
        conn.commit()

        cursor.close()
        conn.close()

        return f"""
            <h3>Factura guardada correctamente</h3>
            <p><b>Cliente:</b> {cliente}</p>
            <p><b>Producto:</b> {producto}</p>
            <p><b>Cantidad:</b> {cantidad}</p>
            <p><b>Precio Unitario:</b> {precio_unitario}</p>
            <hr>
            <p><b>Subtotal:</b> ${subtotal}</p>
            <p><b>IVA (19%):</b> ${iva}</p>
            <p><b>Total a pagar:</b> ${total}</p>
            <br>
            <a href="/menu">Volver al menú</a>
        """

    return """
        <h2>Generar Factura</h2>
        <form method="POST">
            Cliente: <input name="cliente"><br><br>
            Producto: <input name="producto"><br><br>
            Cantidad: <input type="number" name="cantidad"><br><br>
            Precio Unitario: <input type="number" step="0.01" name="precio_unitario"><br><br>
            <button type="submit">Generar</button>
        </form>
        <a href="/menu">Volver al menú</a>
    """
