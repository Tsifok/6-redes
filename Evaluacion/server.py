import threading
import socket
# Se abre la coneccion para recivir usrs
host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Usuarios y contraseñas
array = [
    ("Tsifok","hola"),
    ("Herman","alo22"),
    ("Matias","herman")
]

online_users = []

# Recive al usuario y lo manda a loguearse
def handle():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        # Se manda al loginn
        receive_thread = threading.Thread(target=log_in , args=(client, address))
        receive_thread.start()        

def log_in(client, address):
    # Empieza el login
    flag = True
    while flag:        
        mssg = (f"Debe loguearse antes de mandar algo")        
        client.send(mssg.encode('utf-8'))
        # Debe recivir el /login en esta variable
        log_in = client.recv(1024).decode('utf-8')
        # Si recive el comando lo deja loguearse si
        if(log_in == "/login"):
            # recive la info
            mssg = (f"Ingrese su usuario y luego su contraseña")        
            client.send(mssg.encode('utf-8'))
            usuario = client.recv(1024).decode('utf-8')
            password = client.recv(1024).decode('utf-8')
            # se fija si esta registrado, y si se loguea correctamente
            for usr, passw in array:
                if(usr == usuario and passw == password):
                    global online_users
                    flag = False
                    if online_users:
                        # Deberia verificar si esta conectado
                        for cli, _, usuario_conect in online_users:                        
                            if(usuario_conect == usuario):
                                mssg = (f"Dicho cliente ya esta conectado, ust sera desconectado {usuario_conect}")
                                client.send(mssg.encode('utf-8'))
                                client.close()
                                break
                            else:
                                # Si esta, se loguea y se abre una conexion de mensajes bidireccional
                                # Ademas le dice Bienbenido (*Nombre de usuario*)
                                mssg = (f"Bienbenido {usuario}")
                                client.send(mssg.encode('utf-8'))
                                # Hago que se registren los usuarios qeu estan online                            
                                online_users.append([client, address, usuario])                        
                                flag = False

                                receive_thread = threading.Thread(target=receive , args=(client,))
                                receive_thread.start()
                                receive_thread = threading.Thread(target=write , args=(client,))
                                receive_thread.start()
                    else:
                        mssg = (f"Bienbenido {usuario}")
                        client.send(mssg.encode('utf-8'))
                        # Hago que se registren los usuarios qeu estan online                            
                        online_users.append([client, address, usuario])                        
                        flag = False

                        receive_thread = threading.Thread(target=receive , args=(client,))
                        receive_thread.start()
                        receive_thread = threading.Thread(target=write , args=(client,))
                        receive_thread.start()
                elif flag:
                    # Si su info esta errada, le corta la conexion
                    mssg = (f"Su usuario o contraseña son incorrectos, sera desconectado")        
                    client.send(mssg.encode('utf-8'))

                    #client.close()               
        else:
            # Si no envia el comando correcto le dice y empieza de nuevo
            mssg = (f"Por favor asegurece de escribir solo el comando /login")
            client.send(mssg.encode('utf-8'))
            
        
        
# Para recibir to lo que mande el usr
def receive(client):
    while True:
        try:
            mssg = client.recv(1024).decode('utf-8')
            print(mssg)
        except: 
            print("An error ocurred!")            
            global online_users
            i = 0
            for cli, _, _ in online_users:
                if(client == cli):
                    online_users.remove(online_users[i])
                    client.close()
                else:
                    i = i+1            
            break
# Para mandar strs al usuario
def write(client):  
    while True:      
        mssg = (f"{input()}")
        client.send(mssg.encode('utf-8'))

print(f"Server is listening in port {port}")
handle()
