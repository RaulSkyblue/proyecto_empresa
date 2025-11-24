# src/factura.py
from flask import Blueprint, request, redirect, url_for, session
from db import get_connection
from datetime import datetime

factura_bp = Blueprint("factura", __name__)

def require_login():
    return "user_id" in session

@factura_bp.route("/facturas")
def listar_facturas():
    if not require_login():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Órdenes pendientes (para emitir factura)
    cursor.execute("SELECT * FROM ordenes_compra WHERE estado = 'PENDIENTE'")
    ordenes_pendientes = cursor.fetchall()

    # Facturas emitidas
    cursor.execute("""
        SELECT f.id, f.subtotal, f.iva, f.total, f.fecha, f.estado,
               o.numero_orden, o.cliente
        FROM facturas f
        JOIN ordenes_compra o ON f.orden_id = o.id
        """)
    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    html = "<h1>Facturación</h1>"
    html += "<a href='/menu'>Volver al menú</a><br><br>"

    # ÓRDENES PENDIENTES
    html += "<h2>Órdenes pendientes de facturar</h2>"
    if not ordenes_pendientes:
        html += "<p>No hay órdenes pendientes.</p>"
    else:
        html += """
        <table border="1" cellpadding="5">
          <tr>
            <th>ID Orden</th>
            <th>Número</th>
            <th>Cliente</th>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Precio Unitario</th>
            <th>Acción</th>
          </tr>
        """
        for o in ordenes_pendientes:
            html += f"""
            <tr>
              <td>{o['id']}</td>
              <td>{o['numero_orden']}</td>
              <td>{o['cliente']}</td>
              <td>{o['producto']}</td>
              <td>{o['cantidad']}</td>
              <td>{o['precio_unitario']}</td>
              <td>
                <form method="POST" action="/facturas/emitir">
                  <input type="hidden" name="orden_id" value="{o['id']}">
                  <button type="submit">Emitir factura</button>
                </form>
              </td>
            </tr>
            """
        html += "</table>"

    # FACTURAS EMITIDAS
    html += "<hr><h2>Facturas emitidas</h2>"
    if not facturas:
        html += "<p>No hay facturas registradas.</p>"
    else:
        html += """
        <table border="1" cellpadding="5">
          <tr>
            <th>ID Factura</th>
            <th>Número Orden</th>
            <th>Cliente</th>
            <th>Subtotal</th>
            <th>IVA</th>
            <th>Total</th>
            <th>Fecha</th>
            <th>Estado</th>
          </tr>
        """
        for f in facturas:
            html += f"""
            <tr>
              <td>{f['id']}</td>
              <td>{f['numero_orden']}</td>
              <td>{f['cliente']}</td>
              <td>{f['subtotal']}</td>
              <td>{f['iva']}</td>
              <td>{f['total']}</td>
              <td>{f['fecha']}</td>
              <td>{f['estado']}</td>
            </tr>
            """
        html += "</table>"

    return html

@factura_bp.route("/facturas/emitir", methods=["POST"])
def emitir_factura():
    if not require_login():
        return redirect(url_for("login.login"))

    orden_id = int(request.form["orden_id"])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener la orden
    cursor.execute("SELECT * FROM ordenes_compra WHERE id = %s", (orden_id,))
    orden = cursor.fetchone()

    if not orden:
        cursor.close()
        conn.close()
        return "Orden no encontrada"

    # Calcular montos
    cantidad = orden["cantidad"]
    precio_unitario = float(orden["precio_unitario"])
    subtotal = cantidad * precio_unitario
    iva = round(subtotal * 0.19, 2)
    total = subtotal + iva

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar factura
    cursor2 = conn.cursor()
    cursor2.execute("""
        INSERT INTO facturas (orden_id, subtotal, iva, total, fecha, estado)
        VALUES (%s, %s, %s, %s, %s, 'EMITIDA')
    """, (orden_id, subtotal, iva, total, fecha))

    # Actualizar estado de la orden
    cursor2.execute("UPDATE ordenes_compra SET estado = 'FACTURADA' WHERE id = %s", (orden_id,))

    conn.commit()
    cursor2.close()
    cursor.close()
    conn.close()

    return redirect(url_for("factura.listar_facturas"))
