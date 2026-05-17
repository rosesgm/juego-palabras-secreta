import pymysql
from persistence.db import get_connection
from security.crypto import encrypt, decrypt


class Level:
    """Entidad que representa un nivel del juego."""

    def __init__(self, id: None, level_number: int, title: str,
                 image_filename: str, hint: str, word: str):
        self.id = id
        self.level_number = level_number
        self.title = title
        self.image_filename = image_filename
        self.hint = hint
        self.word = word

    @staticmethod
    def save(level_number: int, title: str, image_filename: str,
             hint: str, word: str) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            encrypted_word = encrypt(word)

            sql = """INSERT INTO level (level_number, title, image_filename, hint, word)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (level_number, title, image_filename,
                                 hint, encrypted_word))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error al guardar el nivel: {e}")
            return False

    @staticmethod
    def get_all():
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM level ORDER BY level_number ASC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [
            Level(
                id=row['id'],
                level_number=row['level_number'],
                title=row['title'],
                image_filename=row['image_filename'],
                hint=row['hint'],
                word=row['word']
            )
            for row in rows
        ]

    @staticmethod
    def get_by_number(level_number: int):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM level WHERE level_number = %s LIMIT 1"
        cursor.execute(sql, (level_number,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row is None:
            return None
        else:
            return Level(
                id=row['id'],
                level_number=row['level_number'],
                title=row['title'],
                image_filename=row['image_filename'],
                hint=row['hint'],
                word=row['word']
            )
        
    @staticmethod
    def update(level_number: int, hint: str, word: str) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            encrypted_word = encrypt(word)

            sql = """UPDATE level 
                    SET hint = %s, word = %s 
                    WHERE level_number = %s"""
            cursor.execute(sql, (hint, encrypted_word, level_number))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error al actualizar el nivel: {e}")
            return False

    def check_answer(self, answer: str) -> bool:
        """Descifra la palabra y compara con la respuesta del jugador."""
        return decrypt(self.word) == answer.lower().strip()  # n
