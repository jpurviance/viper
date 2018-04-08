from client import viper


def times_2(number=None, **kwargs):
    return {"number_x_2": number * 2}

def add_1(number_x_2=None, **kwargs):
    return {"number_plus_1": number_x_2 + 1}

def invert(number_x_2=None, **kwargs):
    return {"number_inverted": -number_x_2}

TASK_NAME = "mytask"
times_task = viper.Task(TASK_NAME, times_2)
add_task = viper.Task("add_task", add_1)
invert_task = viper.Task("invert_task", invert)
times_task >> add_task
times_task >> invert_task
res = times_task.run("localhost:8000", None, {"number": 100})
print(res)
