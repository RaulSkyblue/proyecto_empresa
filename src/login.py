from flask import Blueprint, request, redirect, url_for, session, flash
from src.db import get_db_connection

login_bp = Blueprint("login", __name__)

@login_bp.route("/", methods=["GET", "POST"])
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", 
                       (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("menu.menu_principal"))
        else:
            flash("Usuario o contraseña incorrectos")

    return """
    <h1>Login</h1>
    <form method="POST">
      Usuario:<br><input name="username"><br><br>
      Contraseña:<br><input name="password" type="password"><br><br>
      <button type="submit">Ingresar</button>
    </form>
    """

@login_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login.login"))
