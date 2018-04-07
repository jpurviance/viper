from flask import Flask
from flask import request

app = Flask(__name__)

workers = dict()


@app.route('/')
def hello_world():
    return workers


@app.route("/register")
def register():
    server_name = request.args.get("name")
    server_address = request.args.get("location")
    workers[server_name] = server_address


if __name__ == '__main__':
    app.run()
