#!/bin/sh
source venv/bin/activate
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - mail_forward_flask:app
