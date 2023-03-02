import socket
import threading
import datetime
host = '127.0.0.1'
port = 55555
sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever.bind((host, port))
sever.listen()
clients = []
names = []
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
            if message.startswith('Private Chat'):
                obj_name = message.split('(')[1].split(')')[0]
                message = message.split('): ')[1]
                sub_name = names[clients.index(client)]
                client_obj = clients[names.index(obj_name)]
                client_obj.send(f"{sub_name}:{message}".encode('ascii'))
                client.send(f"{sub_name} : {message}".encode('ascii'))

            elif message.startswith('Group Chat'):

                clients_name=message.split('/')[1].split(',')

                message=message.split('/')[2]

                sub_name = names[clients.index(client)]

                client.send(f"{sub_name} : {message}".encode('ascii'))
                for name in clients_name:
                    clients[names.index(name)].send(f"{sub_name} : {message}".encode('ascii'))

            else:
                client.send("Invalid message format.".encode('ascii'))

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} left the chat'.encode('ascii'))
            names.remove(name)
            break

def receive():
    while True:
        client, address = sever.accept()
        connect_time = datetime.datetime.now()
        client.send('NICK'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        print(f'"{name}" connected with "{str(address)}" at "{connect_time}"')
        names.append(name)
        clients.append(client)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Sever is listening')
receive()
