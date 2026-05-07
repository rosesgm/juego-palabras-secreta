import pymysql
from enums.profile import Profile
from persistence.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id: int, name: str, email: str, password: str, profile: Profile):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile


    def save(name: str, email: str, password: str):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            hash_password = generate_password_hash(password)

            sql = "INSERT INTO user (name, email, password, profile) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, hash_password, 2))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error al guardar el usuario: {e}")
            return False