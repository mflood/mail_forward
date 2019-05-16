FROM python:3.6
ADD flask_app /app
WORKDIR /app
RUN pip install flask gunicorn
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "mail_forward_flask:app"]

#exec gunicorn -b :5000 --access-logfile - --error-logfile - mail_forward_flask:app
