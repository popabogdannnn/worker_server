##VA RULA PE CALULCATOARELE CARE EVALUEAZA WORKER

import socket
import time
import sys
import os
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auxiliary_functions import *

mutex = threading.Lock()

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname() + ".local")
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

job_queue = []

connected = False 
while not connected:
    try:
        client.connect(ADDR)
        connected = True
    except:
        print(f"COULDN'T CONNECT TO MIDDLE [{ADDR}]")
        time.sleep(2)
        connected = False

send_msg(WORKER_MESSAGE, client, True)

def notify_connection(conn):
    while(True):
        mutex.acquire()
        send_msg(STILL_CONNECTED_MESSAGE, conn, True)
        mutex.release()
        time.sleep(0.01)


def handle_eval(conn):
    
    while(True):
        mutex.acquire()
        curr_job = None
        if(len(job_queue) != 0):
            curr_job = job_queue.pop(0)
        mutex.release()
        if(curr_job):
            #start = time.time()
            os.system("mv " + curr_job + " eval/submission.zip")
            os.chdir("eval/")
            os.system("./run_eval.sh")
            os.chdir("../")
            job_json = curr_job.split(".")[0] + ".json"
            os.system("mv eval/" + job_json + " ./")
            mutex.acquire()
            send_file(job_json, conn)
            mutex.release()
            os.system("rm " + job_json)
           # print(time.time() - start)
            



end_connection_thread = threading.Thread(target = notify_connection, args = [client])
end_connection_thread.start()

evaluation_thread = threading.Thread(target = handle_eval, args = [client])
evaluation_thread.start()

while(connected):
    msg = receive_msg(client, True)
   # print(msg)
    if(msg == SEND_FILE_MESSAGE):
        filename = receive_file(client)
        #print("FILE RECEIVED")
        mutex.acquire()
        job_queue.append(filename)
        mutex.release()
    
send_msg(DISSCONNECT_MESSAGE)

client.close()