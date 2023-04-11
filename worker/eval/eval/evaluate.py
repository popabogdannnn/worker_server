import os
import sys
from compile import *
from run_sandbox import *
from run_checker import *
from auxiliary_functions import *

if (len(sys.argv) != 2):
    print("NUMAR INVALID DE ARGUMENTE")
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

if(checker):
    checker_compilation_result = compile("checker.cpp", "checker", checker, instance_name)
#print(compilation_result)

eval_json = {
    "submission_id" : submission_id,
    "compilation": {
    },
    "checker-compilation": {

    } 
}

if(checker):
    eval_json["checker-compilation"]["warnings"] = checker_compilation_result["warnings"]
    if(checker_compilation_result["result"] == "fail"):
        eval_json["checker-compilation"]["compilation"] = "Eroare de compilare la checker!"
    else:
        eval_json["checker-compilation"]["compilation"] = "success"
eval_json["compilation"]["warnings"] = copy.deepcopy(compilation_result["warnings"])

if compilation_result["result"] == "fail":
    eval_json["compilation"]["error"] = "Eroare de compilare!"
elif checker and checker_compilation_result["result"] == "fail":
    pass
else:
    
    eval_json["compilation"]["error"] = "success"
    #test_lines = read_file("tests/tests.txt").split("\n")
    
    test_tags = load_tests()

    cnt = 0
    for tag in test_tags:

        #print(tag)
        in_file_tests = tag + ".in"
        ok_file_tests = tag + ".ok"
        
        if stdio:
            random_file_name = generate_random_string(10)
            in_file = random_file_name + ".in"
            out_file = random_file_name + ".out"
        else:
            in_file = io_filename + ".in"
            out_file = io_filename + ".out"
        ok_file = io_filename + ".ok"

        os.system("rm -rf " + EXECUTION_JAIL +"/*")
        os.system("cp tests/" + in_file_tests + " " + EXECUTION_JAIL + "/" + in_file)
        os.system("echo -n > " + EXECUTION_JAIL + "/" + out_file)
        os.system("cp " + executable_file_name + " " + EXECUTION_JAIL + "/")
        exception_occured = False
        
        try:
            run_info = run_sandbox(executable_file_name, stdio, memory, stack_memory, execution_time, in_file, out_file, instance_name)
        except:
            exception_occured = True
        # !!! BUG NEREZOLVAT DACA CHECKER_JAIL != EXECUTION_JAIL
        test_summary = {

        } 
        if(exception_occured == False):
            test_summary = copy.deepcopy(run_info)
            del test_summary["result"]
        if(exception_occured):
            test_summary["verdict"] = {
                "points_awarded" : 0,
                "reason" : "Exceptie (poate nu sunt vazute toate testele descrise?)"
            }
        elif isinstance(run_info["result"], dict) and "Success" in run_info["result"].keys():
            os.system("cp tests/" + in_file_tests + " " + CHECKER_JAIL + "/" + in_file)
            os.system("cp tests/" + ok_file_tests + " " + CHECKER_JAIL + "/" + ok_file)
            os.system("rm "+ CHECKER_JAIL + "/" + executable_file_name)
            checker_res = run_checker(in_file, out_file, ok_file, execution_time, checker, instance_name)
            test_summary["verdict"] = {
                "points_awarded" : checker_res["p"],
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
        eval_json[cnt] = test_summary 
        cnt += 1  

with open("../" + submission_id + ".json", "w") as f:
    json.dump(eval_json, f, indent = 4)

os.system("rm " + code_file_name)
if compilation_result["result"] == "success":
    os.system("rm " + executable_file_name)
if checker:
    os.system("rm checker.cpp")
    os.system("rm checker")
os.system("rm -rf user_checker/*")
os.system("rm -rf tests/*")
os.system("rm submission_data.json")
os.system("rm *.json")


