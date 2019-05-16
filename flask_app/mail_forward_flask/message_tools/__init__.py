"""
    Utility functions

    * convert_html_to_text
    * validate_email_address
    * text_to_email_addresses

"""
import logging
import re
import html2text
from mail_forward_flask.loggingsetup import APP_LOGNAME

# I pulled this regex from
# https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")

def convert_html_to_text(html):
    """
        Take HTML content and convert to Plaintext
    """
    logger = logging.getLogger(APP_LOGNAME)
    logger.debug("converting html: %s", html)
    as_text = html2text.html2text(html)
    logger.debug("converted to: %s", as_text)
    return as_text


class InvalidEmailException(Exception):
    """
        Thrown when we identify invalid email
    """
    pass

def validate_email_address(email):
    """
        Raises InvalidEmailException if email is not valid
    """
    logger = logging.getLogger(APP_LOGNAME)
    logger.debug("validating email address: '%s'", email)
    try:
        if not EMAIL_REGEX.match(email):
            logger.error("Email address failed validation: '%s'", email)
            raise InvalidEmailException("'{}' failed email regex")
    except TypeError:
        raise InvalidEmailException("'{}' is not a string")

# end
