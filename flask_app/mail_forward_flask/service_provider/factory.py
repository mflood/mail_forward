"""
   service_provider_factory.py
"""
import logging
from mail_forward_flask.service_provider.mailgun import Mailgun
from mail_forward_flask.service_provider.noop import Noop
from mail_forward_flask.loggingsetup import APP_LOGNAME

class ServiceProviderFactoryException(Exception):
    """
        Raised when there is a problem
        creating a service provider
    """
    pass

class ServiceProviderFactory():
    """
        Knows how to configure and build various service providers
    """

    def __init__(self):
        self._mailgun_api_key = None
        self._mailgun_domain = None
        self._default_provider = "noop"
        self._logger = logging.getLogger(APP_LOGNAME)

    def set_default_noop(self):
        """
            Set the default servide provider to noop
        """
        self._default_provider = "noop"

    def set_default_mailgun(self):
        """
            Set the default servide provider to mailgun
        """
        self._default_provider = "mailgun"

    def configure_mailgun(self, api_key, domain):
        """
            Sets configuration info needed to
            instantiate Mailgun instance
        """
        self._mailgun_api_key = api_key
        self._mailgun_domain = domain

    def build_mailgun(self):
        """
            Builds and returns Mailgun
            service provider

            raises ServiceProviderFactoryException
            if it is not configured fully
        """
        self._logger.info("Building Mailgun Service Provider")
        if self._mailgun_api_key and self._mailgun_domain:
            return Mailgun(api_key=self._mailgun_api_key,
                           domain=self._mailgun_domain)

        message = "Mailgun provider not fully configured in Factory"
        self._logger.error(message)
        raise ServiceProviderFactoryException(message)

    def build_noop(self):
        """
            Returns a Noop servicde provider
        """
        self._logger.info("Building Noop Service Provider")
        return Noop()

    def build_default(self):
        """
            Returns a provider based on whether
            self._default_provider is noop, mailgun
        """
        if self._default_provider == "mailgun":
            return self.build_mailgun()

        return self.build_noop()

# end
