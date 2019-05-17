"""
    Flask App for mail_forward
"""
import logging
import json
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from mail_forward_flask.loggingsetup import APP_LOGNAME
from mail_forward_flask.loggingsetup import init_logging
from mail_forward_flask.message_tools.mf_email import MfEmail
from mail_forward_flask.message_tools.mf_email import InvalidMfEmailException

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


@app.route('/email', methods=['POST'])
def email():
    """
        endpoint to forward mail
    """
    content = request.get_json(silent=True)
    as_dict = json.loads(content)
    logger.debug("Request content (%s): %s", type(as_dict), as_dict)
    mf_email = MfEmail()
    try:
        logger.debug("Loading MfEmail")
        mf_email.load_from_dict(dictionary=as_dict)
        logger.debug("Validating MfEmail")
        mf_email.validate()
    except InvalidMfEmailException as error:
        logger.error("MFEmail Error: %s Details: %s", error, error.error_list)
        return jsonify({"status": "error",
                        "message": ["error"],
                        "details": error.error_list})

    logger.debug("Returning ok")
    return jsonify({"status": "ok", "provider": "noop"})

# Uncomment this if you want to invoke the app
# using:
#   python mail_forward_flask/__init__.py
#if __name__ == "__main__":
#    app.run(host='127.0.0.1', port=5000)
