from auxiliary_functions import *

def run_checker(in_file, out_file, ok_file, time, checker, instance_name):
    if checker:
        os.system("cp checker " + CHECKER_JAIL + "/checker")
        os.system("rmdir /sys/fs/cgroup/memory/ia-sandbox/" + instance_name + "/isolated")
        os.system("rmdir /sys/fs/cgroup/memory/ia-sandbox/" + instance_name)
        sandbox_command = "ia-sandbox -r " + PWD + "/" + CHECKER_JAIL
        sandbox_command += " --instance-name " + instance_name
        sandbox_command += " --stdout checker_verdict"
        sandbox_command += " --memory 512mb"
        sandbox_command += " --stack 512mb"
        sandbox_command += " --time " + str(time) + "ms"
        sandbox_command += " --wall-time " + str(time + 2000) + "ms"
        sandbox_command += " -o json"
        sandbox_command += " ./checker"

        sandbox_command = "(" + sandbox_command + ") > checker_data.json"

        os.system(sandbox_command)

        score = 0
        reason = ""
        with open("checker_verdict", "r") as verdict:
            lines = verdict.readlines()    
            if(len(lines) >= 1):
                score = int(lines[0])
            if(len(lines) >= 2):
                reason = lines[1]

        os.system("rm checker_data.json")
        os.system("rm checker_verdict")
        return {"p" : score, "reason" : reason}
    else:
        check = os.system("diff -qBbEa " + CHECKER_JAIL + "/" + out_file + " " + CHECKER_JAIL + "/" + ok_file + "> /dev/null")
        if check == 0:
            return {"p" : 100, "reason" : "Raspuns corect!"}
        else:
            return {"p" : 0, "reason" : "Raspuns gresit!"}
