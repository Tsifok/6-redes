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

        thread = threading.Thread(target=log_in, args=(client,))
        thread.start()

def log_in(client):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            client.send('LOG IN requerido \nIngrese su Email y luego su password'.encode('utf-8'))
            email = client.recv(1024).decode('utf-8')            
            pword = client.recv(1024).decode('utf-8')                        

            # Realizar consultas            
            consulta = f'SELECT COUNT(*) FROM usuarios WHERE email = "{email}" AND pword = "{pword}"'
            cursor.execute(consulta)

            resultados = cursor.fetchall()
            
            

        except Error as e:
            print(f"Error al realizar la consulta: {e}")

print("Server is listening .....")
recive()