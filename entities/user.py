import pymysql
from enums.profile import Profile
from persistence.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# Clase User que contiene los atributos y metodos de un usuario, tambien se encarga de insertar los datos


class User (UserMixin):
    """
    Entidad que representa a un usuario del sistema.
    Hereda de UserMixin para la integración con Flask-Login.
    """

    def __init__(self, id: int, name: str, email: str, password: str, profile: Profile):
        """Constructor de la clase User."""
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile

    def is_admin(self) -> bool:
        """
        Verifica si el usuario actual tiene rol de Administrador.
        
        Returns:
            bool: True si el perfil es ADMIN, False en caso contrario.
        """
        return self.profile == Profile.ADMIN

    @staticmethod
    def save(name: str, email: str, password: str, profile: Profile = Profile.PLAYER) -> bool:
        """
        Guarda un nuevo usuario en la base de datos encriptando su contraseña.
        
        Args:
            name (str): Nombre del usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña en texto plano que se encriptará antes de guardar.
            profile (Profile, optional): Perfil del usuario. Por defecto es PLAYER.
            
        Returns:
            bool: True si el usuario se guardó correctamente, False si hubo un error.
        """
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            hash_password = generate_password_hash(password)

            sql = "INSERT INTO user (name, email, password, profile) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sql, (name, email, hash_password, profile.value))

            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error al guardar el usuario: {e}")
            return False

    @staticmethod
    def check_login(email: str, password: str) -> 'User' | None:
        """
        Verifica las credenciales de inicio de sesión de un usuario.
        
        Args:
            email (str): Correo electrónico del usuario.
            password (str): Contraseña ingresada.
            
        Returns:
            User | None: Retorna el objeto User si las credenciales son válidas, None si fallan.
        """
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, name, email, password, profile FROM user WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user and check_password_hash(user['password'], password):
                return User(user['id'], user['name'], user['email'],
                            user['password'], Profile(user['profile']))
            return None
        except Exception as e:
            print(f"Error al verificar login: {e}")
            return None

    @staticmethod
    def get_by_id(id: int) -> 'User' | None:
        """
        Obtiene un usuario de la base de datos mediante su ID.
        Requerido por Flask-Login para cargar la sesión del usuario.
        
        Args:
            id (int): Identificador único del usuario.
            
        Returns:
            User | None: Retorna el objeto User si existe, None si no se encuentra.
        """
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, name, email, password, profile FROM user WHERE id = %s"
            cursor.execute(sql, (id,))

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:

                return User(user["id"], 
                user["name"], user["email"],
                user["password"], 
                Profile(int(user["profile"])))
            return None
        except Exception as e:
            print(f"Error al obtener el usuario por ID: {e}")
            return None
        
    @staticmethod
    def get_by_email(email: str) -> 'User | None':
        """
        Busca un usuario en la base de datos por su correo electrónico.
        
        Args:
            email (str): Correo a consultar.
            
        Returns:
            User | None: El objeto User si existe, None en caso contrario.
        """
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, name, email, password, profile FROM user WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:
                return User(user["id"], user["name"], user["email"],
                            user["password"], Profile(int(user["profile"])))
            return None
        except Exception as e:
            print(f"Error al obtener el usuario por email: {e}")
            return None
