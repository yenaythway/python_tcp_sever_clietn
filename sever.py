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
###################
#client message ko plane u lr khae
##################
def broadcast(message):
    for client in clients:
        client.send(message)
def groupchat(name_list):
    for name in name_list:
        message=clients[names.index(name)].send(input("Enter your message if u want to quit enter 'b':"))
        # clients[names.index(name)].send(f"{sub_name} : {message}".encode('ascii'))

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

                # clients_name=message.split('/')[1].split(',')
                #
                # message=message.split('/')[2]
                #
                # sub_name = names[clients.index(client)]
                #
                # client.send(f"{sub_name} : {message}".encode('ascii'))
                # for name in clients_name:
                #     clients[names.index(name)].send(f"{sub_name} : {message}".encode('ascii'))

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
        # broadcast(f'{name} join the chat'.encode('ascii'))
        # client.send('Connected to sever and joined the chat'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Sever is listening')
receive()
#
#
# import socket
# import threading
# import datetime
#
# host = '127.0.0.1'
# port = 55555
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((host, port))
# server.listen()
#
# clients = []
# names = {}
#
# def broadcast(message):
#     for client in clients:
#         client.send(message)
#
# def handle(client):
#     while True:
#         try:
#             message = client.recv(1024).decode('ascii')
#             #         name = client.recv(1024).decode('ascii')
#             #         print(f'"{name}" connected with "{str(address)}" at "{connect_time}"')
#             #         names.append(name)
#             #         clients.append(client)
#             #
#             if message.startswith('NICK'):
#                 name = message[5:]
#                 names[client] = name
#                 clients.append(client)
#                 print(f"{name} joined the chat.")
#                 broadcast(f"{name} joined the chat.".encode('ascii'))
#             elif message.startswith('Private Chat'):
#                 obj_name = message.split('(')[1].split(')')[0]
#                 message = message.split('): ')[1]
#                 sub_name = names[client]
#                 client.send(f"{sub_name}:{message}".encode('ascii'))
#                 index=names.
#                 client_obj=clients[names.index(name)]
#
#                 # client.send(f"{sender}:")
#                 # for c, n in names.items():
#                 #     if n == recipient:
#                 #         c.send(f"{sender}: {message}".encode('ascii'))
#                 #         client.send(f"To {recipient}: {message}".encode('ascii'))
#             elif message.startswith('Group Chat'):
#                 recipients = message.split('(')[1].split(')')[0].split(', ')
#                 message = message.split('): ')[1]
#                 sender = names[client]
#                 for c, n in names.items():
#                     if n in recipients:
#                         c.send(f"{sender}: {message}".encode('ascii'))
#                         client.send(f"To {', '.join(recipients)}: {message}".encode('ascii'))
#             else:
#                 client.send("Invalid message format.".encode('ascii'))
#         except:
#             if client in clients:
#                 name = names[client]
#                 clients.remove(client)
#                 del names[client]
#                 print(f"{name} left the chat.")
#                 broadcast(f"{name} left the chat.".encode('ascii'))
#             break
#
# def receive():
#     while True:
#         client, address = server.accept()
#         print(f"Connected with {str(address)} at {datetime.datetime.now()}")
#         client.send('NICK'.encode('ascii'))
#         thread = threading.Thread(target=handle, args=(client,))
#         thread.start()
#
# print("Server is listening...")
# receive_thread = threading.Thread(target=receive)
# receive_thread.start()
