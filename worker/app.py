from flask import Flask, request
import json
import _thread
import time
import requests
import cloudpickle as pickle
import os

f = open("config.json")
config = json.load(f)
config["my_port"] = os.environ.get("port", 5000)
config["my_name"] = os.environ.get("name", "default")
f.close()
requests.post("http://{}:{}/register".format(config["foreman_url"], config["foreman_port"]),
              data={"location": config["my_url"], "port": config["my_port"], "name": config["my_name"]})

app = Flask(__name__)


def do_work(node, kwargs):
    print("started do work")
    start_time = time.time()
    result = node.func(**kwargs)
    node.result = result
    total_time = time.time() - start_time
    node.total_time = total_time
    requests.post("http://{}:{}/completed".format(config["foreman_url"], config["foreman_port"]),
                  data=pickle.dumps((node, result, total_time, config["my_name"])))
    print("work done")


def sleep(args):
    print("sleeping")
    time.sleep(15)


@app.route('/execute', methods=["POST"])
def execute():
    _thread.start_new_thread(do_work, pickle.loads(request.data))
    return ""


if __name__ == '__main__':
    app.run()
