#!/bin/sh
source venv/bin/activate
pip install -e .
coverage run --source mail_forward_flask -m pytest
coverage report -m
