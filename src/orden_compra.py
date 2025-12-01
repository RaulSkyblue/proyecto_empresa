from flask import Blueprint, request
from src.db import get_db_connection

orden_compra_bp = Blueprint('orden_compra', __name__)

@orden_compra_bp.route('/orden', methods=['GET', 'POST'])
def crear_orden():
    if request.method == 'POST':
        cliente = request.form.get('cliente')
        producto = request.form.get('producto')
        cantidad = request.form.get('cantidad')

        conn = get_db_connection()

        # Render (modo demo, sin BD)
        if conn is None:
            return f"""
                <h3>Orden registrada (Demo Render)</h3>
                <p>Cliente: {cliente}</p>
                <p>Producto: {producto}</p>
                <p>Cantidad: {cantidad}</p>
                <p>⚠ No se guardó en base de datos porque Render está en modo demo.</p>
                <a href="/menu">Volver al menú</a>
            """

        # Local (MySQL Laragon)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ordenes (cliente, producto, cantidad) VALUES (%s, %s, %s)",
            (cliente, producto, cantidad)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return "Orden creada correctamente."

    return """
        <h2>Crear Orden de Compra</h2>
        <form method='POST'>
            Cliente: <input name='cliente'><br><br>
            Producto: <input name='producto'><br><br>
            Cantidad: <input name='cantidad' type='number'><br><br>
            <button type='submit'>Crear Orden</button>
        </form>
        <a href="/menu">Volver al menú</a>
    """
