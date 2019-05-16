#!/bin/sh
source activate venv/bin/activate
export FLASK_APP=mail_forward_flask.py
flask run
