# src/orden_compra.py
from flask import Blueprint, request, redirect, url_for, session
from db import get_connection

orden_bp = Blueprint("orden", __name__)

def require_login():
    return "user_id" in session

@orden_bp.route("/ordenes")
def listar_ordenes():
    if not require_login():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ordenes_compra")
    ordenes = cursor.fetchall()
    cursor.close()
    conn.close()

    html = """
    <h1>Órdenes de Compra</h1>
    <a href='/menu'>Volver al menú</a> | 
    <a href='/ordenes/nueva'>Crear nueva orden</a>
    <br><br>
    <table border="1" cellpadding="5">
      <tr>
        <th>ID</th>
        <th>Número</th>
        <th>Cliente</th>
        <th>Producto</th>
        <th>Cantidad</th>
        <th>Precio Unitario</th>
        <th>Estado</th>
      </tr>
    """
    for o in ordenes:
        html += f"""
        <tr>
          <td>{o['id']}</td>
          <td>{o['numero_orden']}</td>
          <td>{o['cliente']}</td>
          <td>{o['producto']}</td>
          <td>{o['cantidad']}</td>
          <td>{o['precio_unitario']}</td>
          <td>{o['estado']}</td>
        </tr>
        """
    html += "</table>"
    return html

@orden_bp.route("/ordenes/nueva", methods=["GET", "POST"])
def nueva_orden():
    if not require_login():
        return redirect(url_for("login.login"))

    if request.method == "POST":
        numero_orden = request.form["numero_orden"]
        cliente = request.form["cliente"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        comuna = request.form["comuna"]
        region = request.form["region"]
        producto = request.form["producto"]
        cantidad = int(request.form["cantidad"])
        precio_unitario = float(request.form["precio_unitario"])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ordenes_compra 
            (numero_orden, cliente, direccion, telefono, comuna, region, producto, cantidad, precio_unitario, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'PENDIENTE')
        """, (numero_orden, cliente, direccion, telefono, comuna, region, producto, cantidad, precio_unitario))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("orden.listar_ordenes"))

    return """
    <h1>Nueva Orden de Compra</h1>
    <form method="POST">
      Número de Orden:<br>
      <input name="numero_orden"><br><br>

      Cliente:<br>
      <input name="cliente"><br><br>

      Dirección:<br>
      <input name="direccion"><br><br>

      Teléfono:<br>
      <input name="telefono"><br><br>

      Comuna:<br>
      <input name="comuna"><br><br>

      Región:<br>
      <input name="region"><br><br>

      Producto:<br>
      <input name="producto"><br><br>

      Cantidad:<br>
      <input name="cantidad" type="number" min="1" value="1"><br><br>

      Precio Unitario:<br>
      <input name="precio_unitario" type="number" step="0.01"><br><br>

      <button type="submit">Guardar</button>
    </form>
    <br>
    <a href="/ordenes">Volver</a>
    """
