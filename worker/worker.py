##VA RULA PE CALULCATOARELE CARE EVALUEAZA WORKER

import socket
import time
import sys
import os
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auxiliary_functions import *

mutex = threading.Lock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

job_queue = []

evaluating = False

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

def handle_eval(conn):
    jobs = 0
    global evaluating
    while(True):
        mutex.acquire()
        curr_job = None
        if(len(job_queue) != 0):
            curr_job = job_queue.pop(0)
        mutex.release()
        if(curr_job):
            start = time.time()
            evaluating = True
            print("EVALUATING : ", curr_job)
            jobs += 1
            print(jobs)
            os.system("mv " + curr_job + " eval/submission.zip")
            os.chdir("eval/")
            os.system("./run_eval.sh")
            os.chdir("../")
            job_json = curr_job.split(".")[0] + ".json"
            os.system("mv eval/" + job_json + " ./")
            mutex.acquire()
            print("TERMINAT")
            send_file(job_json, conn)
            mutex.release()
            os.system("rm " + job_json)
            evaluating = False
            print(time.time() - start)
            

evaluation_thread = threading.Thread(target = handle_eval, args = [client])
evaluation_thread.start()

while(connected):
    msg = receive_msg(client, True)
   # print(msg)
    if(msg == SEND_FILE_MESSAGE):
        filename = receive_file(client)
        #print("FILE RECEIVED")
        job_queue.append(filename)
    
send_msg(DISSCONNECT_MESSAGE)

client.close()