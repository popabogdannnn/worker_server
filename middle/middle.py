##VA RULA PE CALCULATORUL MIDDLE
##PRIMESTE SUBMISII DE LA SERVER SI LE PASEAZA WORKERILOR
##ARE ROL DE LOAD BALANCER

import socket
import threading
from types import BuiltinFunctionType
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auxiliary_functions import *
HEADER = 64
EVAL_REQUEST_MESSAGE = "!EVALUATE!"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname() + ".local")
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISSCONNECT_MESSAGE = "!DISCONNECT!"
WORKER_MESSAGE = "!WORKER!"
OVER_MESSAGE = "!OVER!"
BUFFER_SIZE = 512 * 1024
SEND_FILE_MESSAGE = "!SEND_FILE!"

IP_WHITELIST = [ # MAYBE ADD IT IDK
    SERVER
]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_connection(conn, addr):
    conn.settimeout(1)
    try:
        msg = receive_msg(conn, True)
    except Exception as e:
        print(e)
        print(f"[{addr}] didn't identify")
        return
    conn.settimeout(None)
    if msg == EVAL_REQUEST_MESSAGE:
        handle_evaluation_request(conn, addr)
    if msg == WORKER_MESSAGE:
        handle_worker(conn, addr)

def handle_worker(conn, addr):
    print(f"[{addr}] WORKER connected.")
    connected = True
    while connected:
        msg = recv_message(conn, addr)
        if msg == DISSCONNECT_MESSAGE:
            connected = False
        print(f"[{addr}], {msg}")
    

def handle_evaluation_request(conn, addr):
    print(f"[{addr}] is evaluating")
    msg = receive_msg(conn, True)
    receive_file(conn)
    print(f"[{addr}] done")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()
        #if addr[0] in IP_WHITELIST:
        thread = threading.Thread(target = handle_connection, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



print("[STARTING] server is starting")
start()

