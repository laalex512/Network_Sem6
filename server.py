import socket
import threading

host = "localhost"
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Базу клиентов решил сделать словарем (клиент - ключ, ник - значение)
clients = {}


def send_message(message):
    for i in clients.keys():
        i.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            send_message(message)
        except:
            nickname = clients[client]
            send_message(nickname.encode("ascii") + "left us!")
            client.close()
            clients.pop(client, "Unknown client")
            # если что-нибудь меняется в подключенных клиентах, печатается вся база
            print("Current users:")
            for i in clients.values():
                print(i, end=" ")
            print()
            break


def receive():
    while True:
        client, adress = server.accept()
        print("Connected with " + str(adress), end=". ")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        print("Nickname: " + nickname)
        send_message((nickname + " joined us").encode("ascii"))
        client.send("You're connecting to server!".encode("ascii"))

        clients[client] = nickname
        # если что-нибудь меняется в подключенных клиентах, печатается вся база
        print("Current users:")
        for i in clients.values():
            print(i, end=" ")
        print()

        current_thread = threading.Thread(target=handle, args=(client,))
        current_thread.start()


print("Server get ready")
receive()
