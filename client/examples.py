from client import viper
import time
import json
server = "localhost:8000"
server = "ec2-54-84-252-223.compute-1.amazonaws.com:80"

def times_2(number=None, **kwargs):
    time.sleep(5)
    return {"number_x_2": number * 2}

def add_1(number_x_2=None, **kwargs):
    time.sleep(5)
    return {"number_plus_1": number_x_2 + 1}

def invert(number_plus_1=None, **kwargs):
    time.sleep(5)
    print(number_plus_1)
    return {"number_inverted": -number_plus_1}

times_task = viper.Task("times_task", times_2)
add_task = viper.Task("add_task", add_1)
invert_task = viper.Task("invert_task", invert)

times_task >> add_task >> invert_task

job_id = times_task.run(server, None, {"number": 100})
print(job_id)
while True:
    res = json.loads(viper.get_job_status(server, job_id).decode('ascii'))
    print(res)
    if all(task['status'] == "completed" for task in res):
        break
    time.sleep(5)
result = viper.get_job_results(server, job_id)
print(result)
