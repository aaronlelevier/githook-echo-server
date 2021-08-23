import json

from logzero import logger
from github_webhook import Webhook
from flask import Flask

from echo import git, s3

app = Flask(__name__)
webhook = Webhook(app, endpoint="/")


@webhook.hook(event_type="pull_request")
def pull_request(data):
    """
    Github PR endpoint that performs the following logic

    if this is a PR merge event:
        fetch files to sync
        filter files
        sync files
    """
    logger.info("Event: pull_request")
    logger.info("Data: %s", json.dumps(data))

    if git.is_pr_merge_event(data):
        logger.info("is_pr_merge_event")

        files = git.fetch_files_to_sync(data)
        logger.info("files: %s", files)

        files2 = git.filter_files(files)
        logger.info("filter_files: %s", files2)

        logger.info("start sync")
        s3.sync_files(files2)

    logger.info("done")

    return data
