"""
    Flask App for mail_forward


Environment Variables:

    MF_MAILGUN_API_KEY
    MF_MAILGUN_DOMAIN
    MF_MANDRILL_API_KEY
    MF_DEFAULT_PROVIDER (can be noop, mailgun, mandrill - defaults to mailgun)

"""
import logging
import json
import os
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from mail_forward_flask.loggingsetup import APP_LOGNAME
from mail_forward_flask.loggingsetup import init_logging
from mail_forward_flask.message_tools.mf_email import MfEmail
from mail_forward_flask.message_tools.mf_email import InvalidMfEmailException

from mail_forward_flask.service_provider.factory import ServiceProviderFactory
from mail_forward_flask.service_provider.factory import ServiceProviderFactoryException
from mail_forward_flask.service_provider import ServiceProviderException

# lowercase app is standard name for flask app
# pylint: disable=invalid-name
app = Flask(__name__)

# setup logging
init_logging(logging.DEBUG)
logger = logging.getLogger(APP_LOGNAME)

# configure servicde provider
service_provider_factory = ServiceProviderFactory()
service_provider_factory.configure_mailgun(api_key=os.environ["MF_MAILGUN_API_KEY"],
                                           domain=os.environ["MF_MAILGUN_DOMAIN"])
service_provider_factory.configure_mandrill(api_key=os.environ["MF_MANDRILL_API_KEY"])


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
    #content = request.get_json(silent=True)
    content = request.json
    logger.debug("Incoming request content (%s): %s", type(content), content)
    if isinstance(content, str):
        content = json.loads(content)

    mf_email = MfEmail()
    try:

        # Create email from request
        #
        logger.debug("Loading MfEmail")
        mf_email.load_from_dict(dictionary=content)
        logger.debug("Validating MfEmail")
        mf_email.validate()

        # Build service provider
        #
        if os.environ["MF_DEFAULT_PROVIDER"] == "noop":
            service_provider_factory.set_default_noop()
        elif os.environ["MF_DEFAULT_PROVIDER"] == "mandrill":
            service_provider_factory.set_default_mandrill()
        else:
            service_provider_factory.set_default_mailgun()
        service_provider = service_provider_factory.build_default()
        logger.debug("Using provider %s", service_provider)

        # Send message
        #
        service_provider.send_message(mf_email=mf_email)
        logger.debug("Returning ok")
        return jsonify({"status": "ok", "provider": str(service_provider)})

    except InvalidMfEmailException as error:
        logger.error("MFEmail Error: %s Details: %s", error, error.error_list)
        return jsonify({"status": "error",
                        "message": str(error),
                        "details": error.error_list})

    except ServiceProviderException as error:
        logger.error("ServiceProviderException: %s", error)
        return jsonify({"status": "error",
                        "provider": str(service_provider),
                        "message": str(error),
                        "details": []})


# Uncomment this if you want to invoke the app
# using:
#   python mail_forward_flask/__init__.py
#if __name__ == "__main__":
#    app.run(host='127.0.0.1', port=5000)
