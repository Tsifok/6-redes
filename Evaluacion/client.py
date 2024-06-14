# Importo las librerias a usar
import socket
import threading

# Creo el socket de donde el cliente se va a conectar y le mando que tipo de data va a mandar.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

# Funcion para recivir strings del server 
def receive():
    # Se pone esto para que siempre este activa
    while True:
        try:
            # Recive e imprimme el mensaje
            mssg = client.recv(1024).decode('utf-8')
            print(mssg)
        # En caso de que ocurra un error se le imprime el mensaje al usuario y se le cierra la conexion.
        except: 
            print("An error ocurred!")
            client.close()
            break
# Funcion para mandar todo lo que escriba el cliente en la consola.
def write():  
    # Siempre activa la funcion
    while True:      
        mssg = (f"{input()}")
        client.send(mssg.encode('utf-8'))

# Se crea el hilo para recivir en paralelo
receive_thread = threading.Thread(target=receive)
receive_thread.start()
# Se crea el hilo para mandar mnsjs en paralelo
write_thread = threading.Thread(target=write)
write_thread.start()