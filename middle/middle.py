##VA RULA PE CALCULATORUL MIDDLE
##PRIMESTE SUBMISII DE LA SERVER SI LE PASEAZA WORKERILOR
##ARE ROL DE LOAD BALANCER

import socket
import threading
from types import BuiltinFunctionType
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mutex = threading.Lock()

from auxiliary_functions import *

HEADER = 64

BUFFER_SIZE = 512 * 1024

SLEEP_TIME = 0.3 #HOW MUCH DOES AN EVALUATION THREAD SLEEP SEARCHING FOR ITS JOB 
IP_WHITELIST = [ # MAYBE ADD IT IDK
    SERVER
]

job_queue = []
finished_jobs = set()

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
    conn.settimeout(WORKER_TIMEOUT)
    try:
        while connected:
            msg = receive_msg(conn, addr)
            #print(msg)
            if(msg == ""):
                connected = False
                break
            if msg == DISSCONNECT_MESSAGE:
                connected = False
            if(msg == STILL_CONNECTED_MESSAGE):
                pass
            if msg == SEND_FILE_MESSAGE:
                filename = receive_file(conn)
                mutex.acquire()
                finished_jobs.add(filename)
                mutex.release()
            mutex.acquire()
            if(len(job_queue) != 0 and msg == STILL_CONNECTED_MESSAGE):
                job_name = job_queue.pop(0)
                send_file(job_name, conn)
                os.system("rm " + job_name)
            mutex.release()
    finally:
        print(f"[{addr}] WORKER disconnected.")

    

def handle_evaluation_request(conn, addr):
    #print(f"[{addr}] is evaluating")
    msg = receive_msg(conn, True)
    filename = receive_file(conn)
    
    mutex.acquire()
    job_queue.append(filename)
    mutex.release()
    
    #print(job_queue)

    finished_filename = filename.split(".")[0] + ".json"

    found = False
    start = time.time()
    while not found:
        mutex.acquire()
        if finished_filename in finished_jobs:
            found = True
        mutex.release()
        time.sleep(SLEEP_TIME)
        if(time.time() - start > 30):
            start = time.time()
            print("CAN'T FIND JOB " + finished_filename)
    
    finished_jobs.remove(finished_filename)

    send_file(finished_filename, conn)
    os.system("rm " + finished_filename)

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

