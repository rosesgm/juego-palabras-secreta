from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)

    if user:
        login_user(user)
        return jsonify({"success": True, "message": "Sesión iniciada correctamente"}), 200
    else:
        return jsonify({"success": False, "message": "Correo o contraseña incorrectos."}), 401
@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

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
        
        success = User.save(nombre, email, password,Profile.PLAYER)
        
        if success:
            return jsonify({'message': 'Usuario registrado exitosamente'}), 200
        else:
            return jsonify({'error': 'Error al guardar en la base de datos'}), 500
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error en el servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True)
