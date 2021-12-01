import os
import sys
from compile import *
from run_sandbox import *
from run_checker import *
from auxiliary_functions import *

if (len(sys.argv) != 2):
    print("INVALID NUMBER OF ARGUMENTS")
    exit()

instance_name = sys.argv[1]

code_file_names = {
    "c32" : "main.c",
    "c64" : "main.c",
    "c++32": "main.cpp",
    "c++64": "main.cpp" 
}

executable_file_name = "main"

submission_data = read_json("submission_data.json")

if not submission_data["compiler_type"] in code_file_names.keys():
    print("N-am gasit limbajul")
    exit()

code_file_name = code_file_names[submission_data["compiler_type"]]
submission_id = submission_data["submission_id"]
stdio = submission_data["stdio"]
io_filename = submission_data["io_filename"]
memory = submission_data["memory"]
stack_memory = submission_data["stack_memory"]
execution_time = submission_data["execution_time"]
checker = submission_data["checker"]

compilation_result = compile(code_file_name, executable_file_name, submission_data["compiler_type"], instance_name)

#print(compilation_result)

eval_json = {
    "submission_id" : submission_id,
    "compilation": {
    }
}

eval_json["compilation"]["warnings"] = copy.deepcopy(compilation_result["warnings"])

if compilation_result["result"] == "fail":
    eval_json["compilation"]["error"] = "Eroare de compilare!"
else:

    eval_json["compilation"]["error"] = "success"
    test_lines = read_file("tests/tests.txt").split("\n")

    for line in test_lines:
        line = line.split(' ')
        tag = line[0]
        points = int(line[1])

        in_file_tests = tag + "-" + io_filename + ".in"
        ok_file_tests = tag + "-" + io_filename + ".ok"
        in_file = io_filename + ".in"
        out_file = io_filename + ".out"
        ok_file = io_filename + ".ok"
        
        os.system("rm -rf " + EXECUTION_JAIL +"/*")
        os.system("cp tests/" + in_file_tests + " " + EXECUTION_JAIL + "/" + in_file)
        os.system("echo -n > " + EXECUTION_JAIL + "/" + out_file)
        os.system("cp " + executable_file_name + " " + EXECUTION_JAIL +"/")

        run_info = run_sandbox(executable_file_name, stdio, memory, stack_memory, execution_time, in_file, out_file, instance_name)
      
        # !!! BUG NEREZOLVAT DACA CHECKER_JAIL != EXECUTION_JAIL 
      
        test_summary = copy.deepcopy(run_info)
        del test_summary["result"]
        if isinstance(run_info["result"], dict) and "Success" in run_info["result"].keys():
            os.system("cp tests/" + in_file_tests + " " + CHECKER_JAIL + "/" + in_file)
            os.system("cp tests/" + ok_file_tests + " " + CHECKER_JAIL + "/" + ok_file)
            os.system("rm "+ CHECKER_JAIL + "/" + executable_file_name)
            #os.system("cp checker " + CHECKER_JAIL + "/checker")
            # !!! DE IMPLEMENTAT USER CHECKER
            checker_res = run_checker(in_file, out_file, ok_file, execution_time, checker, instance_name)
            test_summary["verdict"] = {
                "points_awarded" : checker_res["p"] / 100 * points,
                "reason" : checker_res["reason"]
            }
            pass
        else:
            test_summary["verdict"] = {
                "points_awarded" : 0
            }
            if isinstance(run_info["result"], dict):
                for key, value in run_info["result"].items():
                    test_summary["verdict"]["reason"] = str(key) + " " + str(value)
            else:
                test_summary["verdict"]["reason"] = str(run_info["result"])
        eval_json[tag] = test_summary   

with open("../" + submission_id + ".json", "w") as f:
    json.dump(eval_json, f)

os.system("rm " + code_file_name)
if compilation_result["result"] == "success":
    os.system("rm " + executable_file_name)
if checker:
    os.system("rm checker")
os.system("rm -rf user_checker/*")
os.system("rm -rf tests/*")
os.system("rm submission_data.json")

