from flask import Flask
from flask import request
import random
import requests
import queue

app = Flask(__name__)

workers = dict()
available = set()

work_queue = queue.Queue()

class Worker:
    def __init__(self, name, url, port):
        self.name = name,
        self.url = url
        self.port = port

    def __repr__(self):
        return "name: {}, url: {}, port: {}".format(self.name, self.url, self.port)


@app.route('/')
def hello_world():
    return "{}".format(workers)


@app.route("/register", methods=["POST"])
def register():
    worker = Worker(request.form.get("name"), request.form.get("location"), request.form.get("port"))
    workers[request.form.get("name")] = worker
    available.add(request.form.get("name"))
    if not work_queue.empty():
        dispatch_work(*work_queue.get())
    return "bam!"


def dispatch_work(task, args):
    run_on = random.choice(list(available))
    available.remove(run_on)
    run_on_worker = workers[run_on]
    requests.post("http://{}:{}/execute".format(run_on_worker.url, run_on_worker.port))


@app.route("/completed", methods=["POST"])
def completed():
    worker_id = request.form.get("name")
    worker = workers[worker_id]
    available.add(worker)
    if not work_queue.empty():
        dispatch_work(*work_queue.get())
    return ""


@app.route("/run_me")
def run_me():
    work_queue.put((1, 1))
    if len(available) != 0:
        dispatch_work(*work_queue.get())
    return ""


if __name__ == '__main__':
    app.run()
