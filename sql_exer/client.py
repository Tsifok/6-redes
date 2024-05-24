import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

email = ""

def receive():
    while True:
        try:
            mssg = client.recv(1024).decode('utf-8')
            print(mssg)
        except: 
            print("An error ocurred!")
            client.close()
            break

def write():
    while True:
        mssg = (f"{email} : {input()}")
        client.send(mssg.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()