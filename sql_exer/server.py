import threading
import socket 
from config import *

host = '127.0.0.1'
port =  55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

def recive(): 
    while True:
        client, addres = server.accept()
        print(f"Connected with {str(addres)}")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def handle(client):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            client.send('LOG IN requerido \nIngrese su Email y contraseña'.encode('ascii'))
            email, pword = client.recv(1024).decode('ascii')            
            

            # Realizar consultas
            """
            consulta = "SELECT * FROM tu_tabla"
            cursor.execute(consulta)
            
            resultados = cursor.fetchall()
            for fila in resultados:
                print(fila)
            """

        except Error as e:
            print(f"Error al realizar la consulta: {e}")

print("Server is listening .....")
recive()