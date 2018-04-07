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

@app.route('/')
def hello_world():
    return workers


@app.route("/register")
def register():
    server_name = request.args.get("name")
    server_address = request.args.get("location")
    workers[server_name] = server_address


@app.route("/submit", methods=["POST"])
def submit_task():
    print("/submit accessed")
    data = request.data
    graph, args, kwargs = pickle.loads(data)
    result = executor.execute(graph, args, kwargs)
    return send_file(io.BytesIO(pickle.dumps(result, -1)), mimetype="text")






if __name__ == '__main__':
    app.run()
