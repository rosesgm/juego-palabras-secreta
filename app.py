from flask import Flask, Response, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from functools import wraps
from dotenv import load_dotenv
from entities.user import User
from entities.level import Level
from enums.profile import Profile
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

def admin_required(f):
    """
    Decorador de control de acceso basado en roles (RBAC).
    Redirige a los usuarios que no tengan el rol de administrador hacia la vista del juego.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return redirect(url_for('game'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin') if current_user.is_admin() else url_for('game'))
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)

    if user:
        login_user(user)
        return jsonify({"success": True, "redirect": "/admin" if user.is_admin() else "/game"}), 200
    else:
        return jsonify({"success": False, "message": "Correo o contraseña incorrectos."}), 401

@app.route('/admin')
@login_required
@admin_required
def admin(): 
    niveles = Level.get_all()
    return render_template('admin.html', niveles=niveles)

@app.route('/game')
@app.route('/game/<int:num>')
@login_required 
def game(num=0): # Cambiamos a 0 por defecto
    niveles = Level.get_all()
    
    # Evita bucle infinito si la DB está vacía
    if not niveles:
        return render_template('game.html', nivel=None, total=0)
        
    # Si entra directo a /game (num=0), se muestra la bienvenida
    if num == 0:
        return render_template('game.html', welcome=True)
        
    nivel = Level.get_by_number(num)
    
    # Si el nivel no existe, lo manda al primero
    if nivel is None:
        return redirect(url_for('game', num=niveles[0].level_number))
        
    total = len(niveles)
    return render_template('game.html', nivel=nivel, total=total)

@app.route('/api/level', methods=['POST'])
@login_required
def save_level():
    if not current_user.is_admin():
        return jsonify({"success": False, "message": "No autorizado"}), 403

    data = request.get_json()
    level_number = data.get('level_number')
    hint        = data.get('hint')
    word        = data.get('word')

    if not all([level_number, hint, word]):
        return jsonify({"success": False, "message": "Faltan campos"}), 400
        
    success = Level.update(level_number, hint, word)

    if success:
        return jsonify({"success": True, "message": "Nivel guardado"}), 200
    else:
        return jsonify({"success": False, "message": "Error al guardar"}), 500

@app.route('/signup')
def signup() -> Response:
    if current_user.is_authenticated:
        return redirect(url_for('admin') if current_user.is_admin() else url_for('game'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/answer', methods=['POST'])
@login_required
def check_answer():
    data = request.get_json()
    level_number = data.get('level_number')
    answer       = data.get('answer')

    nivel = Level.get_by_number(level_number)
    if nivel is None:
        return jsonify({"success": False, "message": "Nivel no encontrado"}), 404

    if nivel.check_answer(answer):
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "message": "Respuesta incorrecta"}), 200


@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')

        if not nombre or not email or not password:
            return jsonify({
                "success": False,
                "error": "Todos los campos son obligatorios"
            }), 400

        # Verificar si el correo ya está registrado
        if User.get_by_email(email) is not None:
            return jsonify({
                "success": False,
                "error": "El correo electrónico ya se encuentra registrado"
            }), 400

        success = User.save(nombre, email, password, Profile.PLAYER)

        if success:
            return jsonify({'message': 'Usuario registrado exitosamente'}), 200
        else:
            return jsonify({'error': 'Error al guardar en la base de datos'}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error en el servidor'}), 500

@app.route('/victory')
@login_required
def victory():
    return render_template('victory.html')

if __name__ == '__main__':
    app.run(debug=True)
