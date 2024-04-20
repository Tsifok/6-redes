import socket
import threading

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

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print(f"Se ha desconectado {client_address}")
                break
            print(f"Mensaje de {client_address}: {message}")
            #broadcast(message)
        except:
            print(f"Error al recibir mensaje de {client_address}")
            break

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            clients.remove(client)

host = '0.0.0.0'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

print(f"Servidor escuchando en {host}:{port}")

while True:
    client_socket, client_address = server.accept()
    print(f"Conexión entrante de {client_address}")
    clients.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()
"""