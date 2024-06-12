import threading
import socket
from config import *

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

def handle():
    while True:
        client, addres = server.accept()
        print(f"Connected with {str(addres)}")

        thread = threading.Thread(target=log_in, args=(client, addres))
        thread.start()

online_users = []
current_chat = {}

def log_in(client, addres):
    conexion = obtener_conexion()
    flag = True
    if conexion:
        cursor = conexion.cursor()
        while flag:
            try:
                client.send('SERVER: Sesion requerida, ingrese su Email y luego su password'.encode('utf-8'))
                email = client.recv(1024).decode('utf-8')            
                password = client.recv(1024).decode('utf-8')                        
                # Realizar consultas            
                consulta = f'SELECT * FROM usuarios WHERE email = "{email}" AND password = "{password}"'
                cursor.execute(consulta)                
                resultado = cursor.fetchall()
                
                if resultado:
                    username = resultado[0][1]
                    client.send(f'SERVER: Bienvenido {username}, ahora te encuentras en el chat global. Si quieres entrar en un chat privado escribe /email de la persona'.encode('utf-8'))                    
                    global online_users
                    online_users.append([client, addres, username])
                    current_chat[username] = []
                    thread = threading.Thread(target=recive, args=(client, username))
                    thread.start()

                    flag = False
                else:
                    client.send('SERVER: Email o password incorrectos'.encode('utf-8'))

            except Error as e:
                print(f"Error al realizar la consulta: {e}")

def recive(client, username):
    while True:
        msg = client.recv(1024).decode('utf-8')
        # En caso de que quiera hablar con un solo usuario.
        parts = msg.split("/")
        if parts[0] == "" and len(parts) == 2:
            if parts[1] == "all":
                current_chat[username] = []
            else:
                conexion = obtener_conexion()        
                if conexion:
                    cursor = conexion.cursor()
                    consulta = f'SELECT * FROM usuarios WHERE email = "{parts[1]}"'
                    cursor.execute(consulta)                
                    resultado = cursor.fetchall()
                    if not resultado:
                        client.send('SERVER: No se ha podido encontrar al usuario que busca, intentalo nuevamente'.encode('utf-8'))
                    else:
                        current_chat[username] = [parts[1]]
                        client.send(f'SERVER: Ahora te encuentras hablando con {parts[1]}'.encode('utf-8'))

        elif current_chat[username] == []:
            broadcast(msg, username)

        else: 
            private_msg(msg, username, current_chat[username][0])

def broadcast(msg, username):
    for user_client, _, user_name in online_users:
        if user_name != username:
            try:
                user_client.sendall(f'{username}: {msg}'.encode('utf-8'))
            except:
                online_users.remove([user_client, _, user_name])
                user_client.close()

def private_msg(msg, username, target_user):
    for user_client, _, user_name in online_users:
        if user_name == target_user:
            try:
                user_client.sendall(f'{username} (privado): {msg}'.encode('utf-8'))
            except:
                online_users.remove([user_client, _, user_name])
                user_client.close()
            break

print("Server is listening .....")
handle()
