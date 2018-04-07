from flask import Flask, request
import json
import _thread
import time
import requests

f = open("config.json")
config = json.load(f)
f.close()
requests.post("http://{}:{}/register".format(config["foreman_url"], config["foreman_port"]),
              data={"location": config["my_url"], "port": config["my_port"], "name": config["my_name"]})

app = Flask(__name__)


def do_work(job, job_id, job_args):
    print("started do work")
    start_time = time.time()
    result = job(job_args)
    total_time = time.time() - start_time
    requests.post("http://{}:{}/completed".format(config["foreman_url"], config["foreman_port"]),
                  data={"result": result, "job_id": job_id, "name": config["my_name"], "execution_time": total_time})
    print("work done")


def sleep(args):
    print("sleeping")
    time.sleep(15)


@app.route('/execute', methods=["POST"])
def execute():
    _thread.start_new_thread(do_work, (sleep, 123, None,))
    return ""


if __name__ == '__main__':
    app.run()
