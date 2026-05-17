import pymysql
from enums.profile import Profile
from persistence.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# Clase User que contiene los atributos y metodos de un usuario, tambien se encarga de insertar los datos


class User (UserMixin):
    """ Atributos de la clase User """

    def __init__(self, id: int, name: str, email: str, password: str, profile: Profile):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile

    def is_admin(self) -> bool:
        return self.profile == Profile.ADMIN

    """ metodo para guardar un usuario en la base de datos mediante una consulta SQL,
     se utiliza el metodo generate_password_hash para encriptar la contraseña 
     antes de guardarla en la base de datos """

    @staticmethod
    def save(name: str, email: str, password: str, profile: Profile = Profile.PLAYER) -> bool:
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

    """ metodo para verificar el login de un usuario en la base de datos mediante una consulta SQL, se utiliza el metodo check_password_hash para verificar la contraseña """
    @staticmethod
    def check_login(email: str, password: str) -> 'User' | None:
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
