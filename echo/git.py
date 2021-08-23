import base64
import os
import re

import requests

from echo.const import GITHUB_TOKEN


def is_pr_merge_event(event) -> bool:
    """
    Returns bool if this is a PR merge event
    """
    return event["action"] == "closed" and event["pull_request"]["merged"] == True


def fetch_files_to_sync(event) -> dict:
    """
    Fetches all files from PR
    """
    url = f"{event['pull_request']['url']}/files"
    r = _get(url)
    return r.json()


def filter_files(files):
    ret = []

    for f in files:
        if _is_regex_match(f["filename"]) and _is_status_match(f["status"]):

            ret.append(f)

    return ret


def _is_regex_match(filename):
    regexp = r"^(.*?).(yaml|json)$"
    return re.match(regexp, filename)


def _is_status_match(status):
    return status in ("added", "modified")


def fetch_file_contents(url):
    """
    Fetches file contents from Github
    """
    contents_url_response = _get(url)
    data = contents_url_response.json()
    return base64.b64decode(data["content"])


def _get(url):
    return requests.get(
        url, headers={"Authorization": "token %s" % os.environ[GITHUB_TOKEN]}
    )
