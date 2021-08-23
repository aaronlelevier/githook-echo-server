import os
import unittest

from echo.const import GITHUB_TOKEN, BUCKET_NAME


class TestCase(unittest.TestCase):
    def setUp(self):
        os.environ[GITHUB_TOKEN] = "my-token"
        os.environ[BUCKET_NAME] = "my-bucket"
