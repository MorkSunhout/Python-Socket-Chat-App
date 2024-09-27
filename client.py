import socket
import threading
import time
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client, msg):
    try:
        message = msg.encode(FORMAT)
        client.sendall(message)
    except Exception as e:
        print(f"\033[1;31m[ERROR] Failed to send message: {e}\033[0m")

def receive(client):
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message:
                # display messages with a new line and reset the input prompt
                print(f"\r\033[1;34m{message}\033[0m\n\033[1;32m{username}:\033[0m ", end="", flush=True)
        except Exception as e:
            print(f"\033[1;31m[ERROR] {e}\033[0m")
            break

def start():
    global username
    username = input('Enter your username: ')
    answer = input(f'Would you like to connect with username: {username} (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    send(connection, username)

    #  thread to handle incoming messages
    receive_thread = threading.Thread(target=receive, args=(connection,))
    receive_thread.daemon = True  # make sure the thread exits when the main program exits
    receive_thread.start()

    while True:
        msg = input(f"\033[1;32m{username}:\033[0m ")  # display username in green

        if msg.lower() == 'q':
            send(connection, DISCONNECT_MESSAGE)
            break

        send(connection, msg)

    print('\033[1;33mDisconnected\033[0m')  # display disconnect message in yellow
    connection.close()

start()
