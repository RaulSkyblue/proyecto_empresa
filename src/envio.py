# src/envio.py
from flask import Blueprint, request, redirect, url_for, session
from db import get_connection
from datetime import datetime

envio_bp = Blueprint("envio", __name__)

def require_login():
    return "user_id" in session

@envio_bp.route("/envios")
def gestionar_envios():
    if not require_login():
        return redirect(url_for("login.login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Facturas pendientes de envío (EMITIDA)
    cursor.execute("""
        SELECT f.id, f.total, f.fecha, f.estado,
               o.numero_orden, o.cliente
        FROM facturas f
        JOIN ordenes_compra o ON f.orden_id = o.id
        WHERE f.estado = 'EMITIDA'
    """)
    pendientes = cursor.fetchall()

    # Envíos realizados (facturas ENVIADA)
    cursor.execute("""
        SELECT e.id, e.fecha_envio, e.estado_envio, e.observacion,
               f.id AS factura_id, f.total,
               o.numero_orden, o.cliente
        FROM envios e
        JOIN facturas f ON e.factura_id = f.id
        JOIN ordenes_compra o ON f.orden_id = o.id
        WHERE e.estado_envio = 'DESPACHADO'
    """)
    despachados = cursor.fetchall()

    cursor.close()
    conn.close()

    html = "<h1>Gestión de Envíos</h1>"
    html += "<a href='/menu'>Volver al menú</a><br><br>"

    # PENDIENTES
    html += "<h2>Facturas pendientes de envío</h2>"
    if not pendientes:
        html += "<p>No hay facturas pendientes de envío.</p>"
    else:
        html += """
        <table border="1" cellpadding="5">
          <tr>
            <th>ID Factura</th>
            <th>Número Orden</th>
            <th>Cliente</th>
            <th>Total</th>
            <th>Fecha</th>
            <th>Acción</th>
          </tr>
        """
        for f in pendientes:
            html += f"""
            <tr>
              <td>{f['id']}</td>
              <td>{f['numero_orden']}</td>
              <td>{f['cliente']}</td>
              <td>{f['total']}</td>
              <td>{f['fecha']}</td>
              <td>
                <form method="POST" action="/envios/despachar">
                  <input type="hidden" name="factura_id" value="{f['id']}">
                  Observación:<br>
                  <input name="observacion">
                  <br>
                  <button type="submit">Marcar como despachado</button>
                </form>
              </td>
            </tr>
            """
        html += "</table>"

    # DESPACHADOS
    html += "<hr><h2>Envíos despachados</h2>"
    if not despachados:
        html += "<p>No hay envíos despachados.</p>"
    else:
        html += """
        <table border="1" cellpadding="5">
          <tr>
            <th>ID Envío</th>
            <th>ID Factura</th>
            <th>Número Orden</th>
            <th>Cliente</th>
            <th>Total</th>
            <th>Fecha Envío</th>
            <th>Estado Envío</th>
            <th>Observación</th>
          </tr>
        """
        for e in despachados:
            html += f"""
            <tr>
              <td>{e['id']}</td>
              <td>{e['factura_id']}</td>
              <td>{e['numero_orden']}</td>
              <td>{e['cliente']}</td>
              <td>{e['total']}</td>
              <td>{e['fecha_envio']}</td>
              <td>{e['estado_envio']}</td>
              <td>{e['observacion']}</td>
            </tr>
            """
        html += "</table>"

    return html

@envio_bp.route("/envios/despachar", methods=["POST"])
def despachar():
    if not require_login():
        return redirect(url_for("login.login"))

    factura_id = int(request.form["factura_id"])
    observacion = request.form.get("observacion", "")
    fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    # Insertar envío
    cursor.execute("""
        INSERT INTO envios (factura_id, fecha_envio, estado_envio, observacion)
        VALUES (%s, %s, 'DESPACHADO', %s)
    """, (factura_id, fecha_envio, observacion))

    # Actualizar estado de factura
    cursor.execute("""
        UPDATE facturas SET estado = 'ENVIADA' WHERE id = %s
    """, (factura_id,))

    # También podrías marcar la orden como DESPACHADA si quieres:
    cursor.execute("""
        UPDATE ordenes_compra 
        SET estado = 'DESPACHADA'
        WHERE id = (SELECT orden_id FROM facturas WHERE id = %s)
    """, (factura_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("envio.gestionar_envios"))
