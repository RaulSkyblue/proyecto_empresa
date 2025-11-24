from flask import Blueprint, session, redirect, url_for

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu")
def menu_principal():
    if "user_id" not in session:
        return redirect(url_for("login.login"))

    return """
    <h1>Menú Principal</h1>
    <a href='/ordenes'>Órdenes de compra</a><br>
    <a href='/facturas'>Emitir Facturas</a><br>
    <a href='/envios'>Envíos</a><br>
    <a href='/logout'>Cerrar sesión</a><br>
    """
