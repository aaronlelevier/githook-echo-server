from github_webhook import Webhook
from flask import Flask

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"

@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    logger.info("Got push with: %s", data)
    print("Got push with: {}".format(data))
    return data
