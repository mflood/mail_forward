"""
    noop.py
    represents a service provider that does nothing
    is used as the default service provider when
    none of the others are configured
"""
import logging
from mail_forward_flask.service_provider import ServiceProvider
from mail_forward_flask.loggingsetup import APP_LOGNAME

# pylint: disable=too-few-public-methods
class Noop(ServiceProvider):
    """
        Implements ServiceProvider interface
        but does not really send anything
    """
    def __init__(self):
        super(Noop, self).__init__()
        self._logger = logging.getLogger(APP_LOGNAME)

    def __str__(self):
        return "noop"

    def concrete_send_message(self, from_address, to_address, subject, text):
        """
            implementation of send_message
            just prints out args
        """
        self._logger.debug("Noop send_simple_message")
        self._logger.debug("from: %s", from_address)
        self._logger.debug("to: %s", to_address)
        self._logger.debug("subject: %s", subject)
        self._logger.debug("body: %s", text)

#end
