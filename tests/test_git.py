import base64
import os
from unittest.mock import patch, MagicMock

import pretend

from echo import git
from echo.const import GITHUB_TOKEN
from tests.base import TestCase


class GitTests(TestCase):
    def test_is_pr_merge_event_true(self):
        event = {"action": "closed", "pull_request": {"merged": True}}

        ret = git.is_pr_merge_event(event)

        self.assertEqual(ret, True)

    def test_is_pr_merge_event_false(self):
        event = {"action": "closed", "pull_request": {"merged": False}}

        ret = git.is_pr_merge_event(event)

        self.assertEqual(ret, False)

    @patch("echo.git.requests.get")
    def test_fetch_files_to_sync(self, mock_get):
        fake_response = pretend.stub(json=MagicMock())
        mock_get.return_value = fake_response
        event = {
            "action": "closed",
            "pull_request": {
                "merged": True,
                "url": "https://api.github.com/repos/owner/repo/pulls/1",
            },
        }

        ret = git.fetch_files_to_sync(event)

        self.assertEqual(ret, fake_response.json.return_value)
        self.assertEqual(
            mock_get.call_args[0][0],
            "https://api.github.com/repos/owner/repo/pulls/1/files",
        )
        self.assertEqual(
            mock_get.call_args[1],
            {"headers": {"Authorization": f'token {os.environ["GITHUB_TOKEN"]}'}},
        )

    def test_filter_files_is_yaml_or_json(self):
        files = [
            {"filename": "templates/foo.yaml", "status": "added"},
            {"filename": "templates/foo.txt", "status": "added"},
            {"filename": "templates/foo.json", "status": "modified"},
        ]

        ret = git.filter_files(files)

        self.assertEqual(
            ret,
            [
                {"filename": "templates/foo.yaml", "status": "added"},
                {"filename": "templates/foo.json", "status": "modified"},
            ],
        )

    def test_filter_files_is_added_or_modifield(self):
        files = [
            {"filename": "templates/foo.json", "status": "added"},
            {"filename": "templates/bar.json", "status": "modified"},
            {"filename": "templates/biz.json", "status": "removed"},
        ]

        ret = git.filter_files(files)

        self.assertEqual(
            ret,
            [
                {"filename": "templates/foo.json", "status": "added"},
                {"filename": "templates/bar.json", "status": "modified"},
            ],
        )

    @patch("echo.git.requests.get")
    def test_fetch_file_contents(self, mock_get):
        value = b"hello world"
        content = base64.b64encode(value)
        fake_response = pretend.stub(json=MagicMock(return_value={"content": content}))
        mock_get.return_value = fake_response
        url = "https://api.github.com/repos/owner/contents/README.md"

        ret = git.fetch_file_contents(url)

        self.assertEqual(ret, value)
        self.assertEqual(mock_get.call_args[0][0], url)
        self.assertEqual(
            mock_get.call_args[1],
            {"headers": {"Authorization": f'token {os.environ["GITHUB_TOKEN"]}'}},
        )
