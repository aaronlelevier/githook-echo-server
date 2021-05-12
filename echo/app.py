from flask import Flask, request
from logzero import logger


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/post/', methods=['POST'])
def show_post():
    return request.json