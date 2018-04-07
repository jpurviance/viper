from flask import Flask
import requests
import json

f = open("config.json")
config = json.load(f)
f.close()
requests.post("http://{}:{}/register".format(config["foreman_url"], config["foreman_port"]),
              data={"location": config["my_url"], "port": config["my_port"], "name": config["my_name"]})

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
