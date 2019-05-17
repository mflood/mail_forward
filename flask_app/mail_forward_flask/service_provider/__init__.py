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

class ServiceProvider():
    """
        Abstract class represeting
        a service that can send emails
    """

    def __init__(self):
        self._logger = logging.getLogger(APP_LOGNAME)

    def _concrete_send_message(self, from_address, to_address, subject, text):
        """
            This should be implemented in child class to actually send
            an email

            Delivery problems should propagate up using ServiceProviderException
        """
        self._logger.debug("abstract _concrete_send_message: from address: '%s'", from_address)
        self._logger.debug("abstract _concrete_send_message: to address: '%s'", to_address)
        self._logger.debug("abstract _concrete_send_message: subject: '%s'", subject)
        self._logger.debug("abstract _concrete_send_message: body: '%s'", text)

        raise ServiceProviderException("_concrete_send_message not implemented")

    def send_message(self, mf_email):
        """
            Interface method that client should call to send an email

            Raises ServiceProviderException on Failure
        """
        assert isinstance(mf_email, MfEmail)

        from_address = mf_email.get_full_address_from()
        to_address = mf_email.get_full_address_to()
        subject = mf_email.get_subject()
        text = mf_email.get_text()

        self._logger.debug("from address: '%s'", from_address)
        self._logger.debug("to address: '%s'", to_address)
        self._logger.debug("subject: '%s'", subject)
        self._logger.debug("body: '%s'", text)

        # this method needs to exist in descendants
        self._concrete_send_message(from_address=from_address,
                                    to_address=to_address,
                                    subject=subject,
                                    text=text)

# end
