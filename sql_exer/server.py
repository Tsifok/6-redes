import threading
import socket 
from config import *

host = '127.0.0.1'
port =  55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

def handle(): 
    while True:
        client, addres = server.accept()
        print(f"Connected with {str(addres)}")

        thread = threading.Thread(target=log_in, args=(client,))
        thread.start()

def log_in(client):
    conexion = obtener_conexion()
    flag = True
    if conexion:
        cursor = conexion.cursor()
        while(flag):
            try:
                client.send('LOG IN requerido \nIngrese su Email y luego su password'.encode('utf-8'))
                email = client.recv(1024).decode('utf-8')            
                password = client.recv(1024).decode('utf-8')                        

                # Realizar consultas            
                consulta = f'SELECT * FROM usuarios WHERE email = "{email}" AND password = "{password}"'
                cursor.execute(consulta)
                
                resultado = cursor.fetchall()
                print(resultado) 
                
                if resultado:
                    client.send('Login exitoso'.encode('utf-8'))
                    flag = False

                else:
                    client.send('Email o password incorrectos'.encode('utf-8'))

            except Error as e:
                print(f"Error al realizar la consulta: {e}")

def msg():
    print("")    




print("Server is listening .....")
handle()