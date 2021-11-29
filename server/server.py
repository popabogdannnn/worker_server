##VA RULA PE SERVERUL VCODERS

import socket
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auxiliary_functions import *

if len(sys.argv) != 2:
    print("INVALID NUMBER OF ARGUMENTS")
    exit()

filename = sys.argv[1]
EVAL_REQUEST_MESSAGE = "!EVALUATE!"
PORT = 5050
MIDDLE = socket.gethostbyname(socket.gethostname() + ".local")
ADDR = (MIDDLE, PORT)
DISSCONNECT_MESSAGE = "!DISCONNECT!"
OVER_MESSAGE = "!OVER!"
FORMAT = 'utf-8'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
while not connected:
    try:
        client.connect(ADDR)
        connected = True
    except:
        print(f"COULDN'T CONNECT TO MIDDLE [{ADDR}]")
        time.sleep(2)
        connected = False


send_msg(EVAL_REQUEST_MESSAGE, client, True)

send_file(filename, client)


client.close()

