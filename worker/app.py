from flask import Flask
import requests
import json


with open("config.json") as config_json:
    config = json.load(config_json)
    print(config)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
