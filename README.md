# Readme

This project usings [github-webhook](https://github.com/bloomberg/python-github-webhook) and:

- echos the Git hook request data received from Github
- checks for a PR merge event
- syncs files to an S3 bucket that match a path regex (currently hardcoded)

## Status

This project currently only works locally.

## Setup

These enviroment variables must be set:

- GITHUB_TOKEN - valid github token to read files from your repo where you receive the PR event
- BUCKET_NAME - name of S3 bucket to sync matching files to

Create a virtualenv with Python 3.8 (as tested) and:

```
pip install -r requirements.txt
pip install -e .
```

## Usage

Run these first 2 commands to start Ngrok and the flask app:

Commands to start [ngrok](https://ngrok.com/) and tunnel to a local [Flask](https://flask.palletsprojects.com) app:

```bash
# start ngrok
ngrok http 5000

# activate virtualenv
source venv/bin/activate

# cd to flask app dir
cd echo

# start flask server
python -m flask run
```

Configure a new webhook on the Github repo for Pull Request events with the URL from Ngrok.

Submit a PR to the Github repo that you just configures, merge, and on merge the matching files via the logic in `echo.git.filter_files` will be merged to the S3 bucket

## Testing

```
python -m unittest
```

## Future

Some future things would be:

- [ ] Move filtering logic of what files to sync to a config file
- [ ] Allow a S3 key prefix to be used for where to store the files in the S3 bucket
- [ ] Productionalize
- [ ] Github token should be fetched from a secret vault
