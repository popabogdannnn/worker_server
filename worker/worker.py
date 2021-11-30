##VA RULA PE CALULCATOARELE CARE EVALUEAZA WORKER

import socket
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auxiliary_functions import *

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname() + ".local")
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISSCONNECT_MESSAGE = "!DISCONNECT!"
WORKER_MESSAGE = "!WORKER!"

start = time.time()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



client.close()