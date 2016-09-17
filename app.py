import os
import json

import requests
import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = int(os.environ.get('PORT', 3000)))
