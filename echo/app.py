from logzero import logger
from github_webhook import Webhook
from flask import Flask

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"

@webhook.hook(event_type="pull_request")
def on_push(data):
    logger.info("Got push with: %s", data)
    print("Got push with: {}".format(data))

    return data
