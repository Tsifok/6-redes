import socket
import threading

nickname = input("Input your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

def receive():
    while True:
        try:
            mssg = client.recv(1024).decode('ascii')
            if mssg == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(mssg)
        except: 
            print("An error ocurred!")
            client.close()
            break

def write():
    while True:
        mssg = f"{nickname} : {input("")}"
        client.send(mssg.encode('ascii'))

receive_thread = threading.Thread(target="receive")
receive_thread.start()

write_thread = threading.Thread(target="write")
write_thread.start()