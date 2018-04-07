from flask import Flask
from flask import request
from flask import send_file
import io
import uuid
import cloudpickle as pickle

from common import executor
app = Flask(__name__)

workers = dict()
tasks = dict()

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
    return "bam!"


@app.route("/submit", methods=["POST"])
def submit_task():
    print("/submit accessed")
    data = request.data
    graph, args, kwargs = pickle.loads(data)
    result = executor.execute(graph, args, kwargs)
    return send_file(io.BytesIO(pickle.dumps(result, -1)), mimetype="text")






if __name__ == '__main__':
    app.run()
