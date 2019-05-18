"""
    __init__.py
    Defines abstract ServiceProvider class and exception
"""
import logging
from mail_forward_flask.message_tools.mf_email import MfEmail
from mail_forward_flask.loggingsetup import APP_LOGNAME

class ServiceProviderException(Exception):
    """
        When when send_message fails
    """
    pass

# pylint: disable=too-few-public-methods
class ServiceProvider():
    """
        Abstract class represeting
        a service that can send emails
    """

    def __init__(self):
        self._logger = logging.getLogger(APP_LOGNAME)

    def __str__(self):
        return "AbstractServiceProvider"

    def concrete_send_message(self, mf_email):
        """
            This should be implemented in child class to actually send
            an email

            Delivery problems should propagate up using ServiceProviderException
        """
        self._logger.debug("mf_email: '%s'", mf_email)

        raise ServiceProviderException("concrete_send_message not implemented")

    def send_message(self, mf_email):
        """
            Interface method that client should call to send an email

            Raises ServiceProviderException on Failure
        """
        assert isinstance(mf_email, MfEmail)

        # this method needs to exist in descendants
        self.concrete_send_message(mf_email=mf_email)

# end
