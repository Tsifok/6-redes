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




































"""
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Error al recibir mensaje del servidor")
            break

host = 'localhost'
port = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input()
    client_socket.send(message.encode())
"""