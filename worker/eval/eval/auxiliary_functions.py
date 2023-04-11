import json
import os
import copy
import glob
import string    
import random

PWD = os.getcwd()
COMPILATION_JAIL = "jail"
EXECUTION_JAIL = "jail"
CHECKER_JAIL = "jail"

def read_json(file_name):
    file_submission_data = open(file_name)
    return json.load(file_submission_data)

def read_file(file_name):
    file = open(file_name, mode = 'r')
    all_of_it = file.read()
    return all_of_it

def load_tests():
    os.chdir("tests")
    test_list = []
    for file in glob.glob("*.in"):
        test_tag = file.split(".")[0]
        if(os.path.exists(f"{test_tag}.ok")):
            test_list.append(test_tag)
    os.chdir("..")
    test_list.sort()
    return test_list   

def generate_random_string(length):
    result = ''.join((random.choice(string.ascii_lowercase) for x in range(length)))
    return result