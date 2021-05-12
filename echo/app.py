from logzero import logger
from github_webhook import Webhook
from flask import Flask

app = Flask(__name__)
webhook = Webhook(app, endpoint="/pull-request")


@webhook.hook(event_type="pull_request")
def pull_request(data):
    logger.info("%s", data)
    return data
