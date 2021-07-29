import json

from logzero import logger
from github_webhook import Webhook
from flask import Flask

app = Flask(__name__)
webhook = Webhook(app, endpoint="/")


@webhook.hook(event_type="pull_request")
def pull_request(data):
    logger.info("Event: pull_request")
    logger.info("%s", data)
    return data

@webhook.hook(event_type="pull_request_review")
def pull_request_review(data):
    logger.info("Event: pull_request_review")
    logger.info("%s", data)
    return data

@webhook.hook(event_type="pull_request_review_comment")
def pull_request_review_comment(data):
    logger.info("Event: pull_request_review_comment")
    logger.info("%s", data)
    return data
