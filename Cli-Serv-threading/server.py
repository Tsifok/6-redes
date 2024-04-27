import socket

# Configurar el servidor
host = "127.0.0.1"
port = 5555

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        
    # Enlazar el socket al host y al puerto
    server_socket.bind((host, port))
        
    print(f"Escuchando en el puerto {port} si")
    # Escuchar conexiones entrantes
    server_socket.listen()
    print("Servidor escuchando en {}:{}...".format(host, port))

    # Aceptar la conexión entrante
    client_socket, client_address = server_socket.accept()
    #print("Cliente {}:{} conectado.".format(client_address[0], client_address[1]))

        # Iniciar el chat
    while True:
            # Recibir mensaje del cliente
        client_message = client_socket.recv(1024).decode("utf-8")
        if not client_message:
            break
        #print(f"{client_address[0]} : {data.decode('utf-8')}")
        print("Cliente: {}".format(client_message))

            # Enviar mensaje al cliente
        server_message = input("Servidor: ")
        client_socket.sendall(server_message.encode("utf-8"))

    # Cerrar la conexión
client_socket.close()
server_socket.close()


"""

socket.AF_INET: Este argumento especifica que el socket será de tipo AF_INET, que es la familia de direcciones para IPv4. 
Indica que el socket utilizará direcciones IPv4 para la comunicación en red.

socket.SOCK_STREAM: Este argumento especifica el tipo de socket, en este caso SOCK_STREAM, que indica que el socket será de tipo flujo. 
Los sockets de flujo proporcionan una conexión bidireccional 

"""

"""
HOST = "127.0.0.1"
PORT = 38616

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print(f"Escuchando en el puerto {PORT} si")
    s.listen()
    conn, addr  = s.accept()
    with conn:
        print(f"Conectado a {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                print("cloasing conn")
                break
            #s.send(data)
            print(f"{addr[0]} : {data.decode('utf-8')}")
"""