##VA RULA PE CALULCATOARELE CARE EVALUEAZA WORKER

from concurrent.futures import thread
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

def handle_eval(conn, run_event):
    jobs = 0
    global evaluating
    x = 0
    while(run_event.is_set()):
        x += 1
        if(x == 10):
            print("CAUT!")
            x = 0
        mutex.acquire()
        curr_job = None
        if(len(job_queue) != 0):
            curr_job = job_queue.pop(0)
        else:
            time.sleep(1)
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
            


run_event = threading.Event()
run_event.set()
evaluation_thread = threading.Thread(target = handle_eval, args = [client, run_event])
evaluation_thread.start()

try:
    while(connected):
        msg = receive_msg(client, True)
        print(msg)
        if(msg == SEND_FILE_MESSAGE):
            filename = receive_file(client)
            print("FILE RECEIVED")
            mutex.acquire()
            job_queue.append(filename)
            mutex.release()
        if(msg == DISSCONNECT_MESSAGE):
            run_event.clear()
            evaluation_thread.join()
            connected = False
            send_msg(DISSCONNECT_MESSAGE, client, True)
            client.close()
except KeyboardInterrupt:
    run_event.clear()
    evaluation_thread.join()
    send_msg(DISSCONNECT_MESSAGE, client, True)
    client.close()
    
