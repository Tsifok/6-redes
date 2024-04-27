import socket

host = "127.0.0.1"
port = 5555

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    # Conectar el socket al servidor
    client_socket.connect((host, port))
    print("Conectado al servidor.")

    # Iniciar el chat
    while True:
        # Enviar mensaje al servidor
        client_message = input("Cliente: ")
        client_socket.sendall(client_message.encode("utf-8"))

        # Salir si el mensaje es "adios"
        if client_message.lower() == "adios":
            break

        # Recibir mensaje del servidor
        server_message = client_socket.recv(1024).decode("utf-8")
        print("Servidor:", server_message)

    # Cerrar la conexión
    client_socket.close()


"""

import socket
import threading

HOST = "127.0.0.1" 
PORT = 38616

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        msj = input("msj: ")
        s.send(bytes(msj, "utf-8"))
        data = s.recv(1024)
   
print(f"Recibido {data!r}")    

1 Cliente(s) servidor threading, el cliente se debe autentificar (lo primero que aparece usuario contraseña) si no esta autentificado cierra conexion
2 El cliente a travez de un menu (opc 1 2 3 4 ) 
    1 chat simple cliente servidor ()
    2 Enviar un mensaje broker(a todos los clientes conectados)


"""