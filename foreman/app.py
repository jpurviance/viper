from flask import Flask, request, send_file
import random
import requests
import queue
import io
import uuid
import cloudpickle as pickle

from common import executor

app = Flask(__name__)

workers = dict()

available = set()

work_queue = queue.Queue()

executors = {}


class Worker:
    def __init__(self, name, url, port):
        self.name = name,
        self.url = url
        self.port = port

    def __repr__(self):
        return "<Worker name: {}, url: {}, port: {}>".format(self.name, self.url, self.port)


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
    requests.post("http://{}:{}/execute".format(run_on_worker.url, run_on_worker.port),
                  data=pickle.dumps((task, args)))


@app.route("/completed", methods=["POST"])
def completed():
    node, result, total_time, worker_id = pickle.loads(request.data)
    exec = executors[node.job_id]
    node.result = result
    node.total_time = total_time
    for item in exec.step(node):
        work_queue.put(item)
    worker = workers[worker_id]
    available.add(worker_id)
    while available and not work_queue.empty():
        dispatch_work(*work_queue.get())
    return ""


@app.route("/run_me")
def run_me():
    work_queue.put((1, 1))
    if len(available) != 0:
        dispatch_work(*work_queue.get())
    return ""


@app.route("/job_status", methods=["POST"])
def job_status():
    job_id = request.form.get("job_id")
    return executors[job_id].get_status()


@app.route("/submit", methods=["POST"])
def submit_task():
    graph, args, kwargs = pickle.loads(request.data)
    job_id = str(uuid.uuid4())
    exec = executor.Executor(graph, args, kwargs, job_id)
    for item in exec.step({}):
        work_queue.put(item)
    executors[job_id] = exec
    while available and not work_queue.empty():
        dispatch_work(*work_queue.get())
    return job_id


@app.route("/hello_world")
def hello():
    return "Hello World"


@app.route("/submit_debug", methods=["POST"])
def submit_task_debug():
    graph, args, kwargs = pickle.loads(request.data)
    result = executor.execute(graph, args, kwargs)
    return send_file(io.BytesIO(pickle.dumps(result, -1)), mimetype="text")


if __name__ == '__main__':
    app.run()
