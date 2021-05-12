from flask import Flask, request
from logzero import logger


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/post/', methods=['POST'])
def show_post():
    logger.info('vars: %s', vars(request))
    logger.info('json: %s', request.json)
    return request.json
