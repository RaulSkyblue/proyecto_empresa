from flask import Blueprint, request, redirect, url_for
from src.db import get_db_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')

        # Obtener conexión
        conn = get_db_connection()
        if conn is None:
            # Render → sin BD
            if usuario == "admin" and clave == "admin":
                return redirect(url_for('menu.menu'))
            return "BD desactivada en Render: solo puedes usar usuario=admin, clave=admin"

        # LOCAL (Laragon)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=%s AND clave=%s",
            (usuario, clave)
        )

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return redirect(url_for('menu.menu'))
        else:
            return "Usuario o clave incorrectos"

    return """
        <h2>Login</h2>
        <form method='POST'>
            Usuario: <input name='usuario'>
            Clave: <input name='clave' type='password'>
            <button type='submit'>Ingresar</button>
        </form>
    """
