import base64
import os
from unittest.mock import patch, MagicMock

import pretend

from echo import s3
from echo.const import BUCKET_NAME
from tests.base import TestCase


class S3Tests(TestCase):
    @patch("echo.s3.get_boto_client")
    @patch("echo.s3.git.fetch_file_contents")
    def test_sync_files(self, mock_fetch_file_contents, mock_get_boto_client):
        # mock_get_boto_client - setup
        client = pretend.stub(put_object=MagicMock())
        mock_get_boto_client.return_value = client
        # mock_fetch_file_contents - setup
        value = b"hello world"
        mock_fetch_file_contents.return_value = value
        # files
        files = [
            {
                "filename": "templates/foo.json",
                "status": "added",
                "contents_url": "URL-A",
            },
        ]

        ret = s3.sync_files(files)

        self.assertEqual(ret, ["templates/foo.json"])
        self.assertEqual(mock_get_boto_client.call_count, 1)
        self.assertEqual(mock_get_boto_client.call_args[0], ("s3",))
        self.assertEqual(mock_fetch_file_contents.call_count, 1)
        self.assertEqual(mock_fetch_file_contents.call_args[0], ("URL-A",))
        self.assertEqual(client.put_object.call_count, 1)
        self.assertEqual(
            client.put_object.call_args[1],
            {
                "Bucket": os.environ[BUCKET_NAME],
                "Key": "templates/foo.json",
                "Body": value,
            },
        )
