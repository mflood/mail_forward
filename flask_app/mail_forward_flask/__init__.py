"""
    Flask App for mail_forward
"""
import logging
from flask import Flask
from flask import render_template
from mail_forward_flask.loggingsetup import APP_LOGNAME
from mail_forward_flask.loggingsetup import init_logging

# lowercase app is standard name for flask app
# pylint: disable=invalid-name
app = Flask(__name__)

# setup logging
init_logging(logging.DEBUG)
logger = logging.getLogger(APP_LOGNAME)

@app.route("/")
def index():
    """
        endpoint for app main page
    """
    logger.debug("Rendering index.html")
    return render_template('index.html')

# Uncomment this if you want to invoke the app
# using:
#   python mail_forward_flask/__init__.py
#if __name__ == "__main__":
#    app.run(host='127.0.0.1', port=5000)
