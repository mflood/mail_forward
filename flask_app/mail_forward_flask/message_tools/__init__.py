"""
    Utility functions

    * convert_html_to_text
    * validate_email_address
    * text_to_email_addresses

"""
import logging
import html2text
from mail_forward_flask.loggingsetup import APP_LOGNAME

def convert_html_to_text(html):
    """
        Take HTML content and convert to Plaintext
    """
    logger = logging.getLogger(APP_LOGNAME)
    logger.debug("converting html: %s", html)
    as_text = html2text.html2text(html)
    logger.debug("converted to: %s", as_text)
    return as_text

# end
