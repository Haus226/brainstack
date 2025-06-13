import socket
import threading

HOST = '192.168.1.115' 
PORT = 5000
clients: dict[str, socket.socket] = {}
addresses: dict[socket.socket, str] = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"[SERVER] Listening on {HOST}:{PORT}")

def broadcast(message):
    for client in clients.values():
            client.send(message)

def handle(client:socket.socket):
    try:
        name = client.recv(1024).decode()
        # User and socket pairs
        clients[name] = client
        addresses[client] = name
        broadcast(f"[SERVER] {name} joined the chat.\n".encode())

        while True:
            msg = client.recv(1024)
            if not msg:
                break
            if msg.startswith(b"/msg:"):
                _, to_user, pm = msg.decode().split(":", 2)
                if to_user in clients:
                    clients[to_user].send(f"[PM from {name}]: {pm}\n".encode())
                else:
                    client.send(f"[SERVER] User {to_user} not found.\n".encode())
            else:
                broadcast(f"<{name}>: {msg.decode()}\n".encode())

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()
        if client in addresses:
            left_name = addresses[client]
            del clients[left_name]
            del addresses[client]
            broadcast(f"[SERVER] {left_name} left the chat.\n".encode())

def main():
    while True:
        client, addr = server.accept()
        print(f"[CONNECTED] {addr}")
        threading.Thread(target=handle, args=(client, )).start()

main()
