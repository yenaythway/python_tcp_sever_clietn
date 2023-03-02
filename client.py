
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
name = input('Enter your name: ')

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(name.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occurred!')
            client.close()
            break

def write():
    while True:
        print("Choose an option:\n1. Group chat\n2. Private chat\n")
        option = input("Enter your choice (1/2): \n")

        if option == "1":
            clients=input("Enter client names separated by commas (e.g. John, Sarah):")
            message = input("Enter your message ")
            message = f"Group Chat /{clients}/{name}:{message}"
            client.send(message.encode('ascii'))


        elif option == "2":
            client_name=input("Enter client name:")
            message = input("Enter your message: ")
            message = f"Private Chat ({client_name}): {message}"
            client.send(message.encode('ascii'))

        else:
            print("Invalid option! Please enter a valid choice.")

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()

