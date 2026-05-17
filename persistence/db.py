import pymysql

#cada quien tiene que configurar su propia conexion a la base de datos, con sus credenciales y nombre de la base de datos
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='admin',
        database='crossover_db'
    )
