import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pruebe"
        )

        if conn.is_connected():
            print("Conexión exitosa a la base de datos")
            return conn  # Retorna la conexión si es exitosa
        else:
            print("No se pudo conectar a la base de datos")
            return None

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
