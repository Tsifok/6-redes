import mysql.connector
from mysql.connector import Error

class DatabaseHandler:
    def __init__(self):
        self.connection = self.obtener_conexion()
    
    def obtener_conexion(self):
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

    def new_msg(self, msg, source, destination = None):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                if destination == None:
                    query = f'INSERT INTO mensajes (id_origen, mensaje) VALUES ({source}, "{msg}")'
                else:
                    query = f'INSERT INTO mensajes (id_origen, id_destino, mensaje) VALUES ({source}, {destination}, "{msg}")'
                cursor.execute(query)
                self.connection.commit()
                print("Mensaje insertado correctamente")
            except Error as e:
                print(f"Error al insertar el mensaje: {e}")
        else:
            print("No hay conexión a la base de datos")