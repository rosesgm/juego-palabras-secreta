import pymysql


def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='64571ok.',
        database='crossover_db'
    )
