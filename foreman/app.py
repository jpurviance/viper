from flask import Flask
from flask import request

app = Flask(__name__)

workers = dict()


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


if __name__ == '__main__':
    app.run()
