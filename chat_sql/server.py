import threading
import socket
import mysql.connector
from mysql.connector import Error as MySQLError  # Renombrar Error de mysql.connector para evitar conflictos

from database_handler import DatabaseHandler  # Importa la clase del archivo separado

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

db_handler = DatabaseHandler()  # Crea una instancia de la clase DatabaseHandler

def handle():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        thread = threading.Thread(target=log_in, args=(client, address))
        thread.start()

online_users = []
current_chat = {}

def log_in(client, address):
    flag = True
    if db_handler.connection:
        cursor = db_handler.connection.cursor()
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
                    username_id = resultado[0][0]
                    client.send(f'SERVER: Bienvenido {username}, ahora te encuentras en el chat global. Si quieres entrar en un chat privado escribe /email de la persona'.encode('utf-8'))                    
                    global online_users
                    online_users.append([client, address, username, username_id])
                    current_chat[username] = []
                    thread = threading.Thread(target=recive, args=(client, username, username_id))
                    thread.start()

                    flag = False
                else:
                    client.send('SERVER: Email o password incorrectos'.encode('utf-8'))

            except MySQLError as e:
                print(f"Error al realizar la consulta MySQL: {e}")
            except Exception as e:
                print(f"Error general al realizar la consulta: {e}")

def recive(client, username, username_id):
    while True:
        msg = client.recv(1024).decode('utf-8')
        # En caso de que quiera hablar con un solo usuario.
        parts = msg.split("/")
        if parts[0] == "" and len(parts) == 2:
            if parts[1] == "all":
                current_chat[username] = []
            else:
                if db_handler.connection:
                    cursor = db_handler.connection.cursor()
                    consulta = f'SELECT * FROM usuarios WHERE email = "{parts[1]}"'
                    cursor.execute(consulta)                
                    resultado = cursor.fetchall()
                    if not resultado:
                        client.send('SERVER: No se ha podido encontrar al usuario que busca, intentalo nuevamente'.encode('utf-8'))
                    else:
                        current_chat[username] = [parts[1]]
                        client.send(f'SERVER: Ahora te encuentras hablando con {parts[1]}'.encode('utf-8'))

        elif current_chat[username] == []:
            broadcast(msg, username, username_id)

        else: 
            private_msg(msg, username, username_id, current_chat[username][0])

def broadcast(msg, username, username_id):
    global online_users
    #Archivo el mensaje en la base de datos
    db_handler.new_msg(msg, username_id)
    for user_client, _, user_name, _ in online_users:
        if user_name != username:
            try:
                user_client.sendall(f'{username}: {msg}'.encode('utf-8'))                
            except Exception as e:
                print(f"Error al enviar mensaje a {user_name}: {e}")
                online_users = [user for user in online_users if user[2] != user_name]
                user_client.close()

def private_msg(msg, username, username_id, target_user):
    global online_users
    for user_client, _, user_name, user_id in online_users:
        if user_name == target_user:
            try:
                user_client.sendall(f'{username} (privado): {msg}'.encode('utf-8'))
                #Archivo el mensaje en la base de datos
                db_handler.new_msg(msg, username_id, user_id)
            except Exception as e:
                print(f"Error al enviar mensaje privado a {user_name}: {e}")
                online_users = [user for user in online_users if user[2] != user_name]
                user_client.close()
            break

print("Server is listening .....")
handle()
