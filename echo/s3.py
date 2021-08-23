import os
import io

import base64
import boto3

from echo import git
from echo.const import BUCKET_NAME


def get_boto_client(aws_service, **kwargs):
    return boto3.client(aws_service, **kwargs)


def sync_files(files):
    """
    Syncs files to S3
    """
    ret = []

    client = get_boto_client("s3")

    for f in files:

        # TODO(aaronlelevier): log or check response
        client.put_object(
            Bucket=os.environ[BUCKET_NAME],
            Key=f["filename"],
            Body=git.fetch_file_contents(f["contents_url"]),
        )

        ret.append(f["filename"])

    return ret
