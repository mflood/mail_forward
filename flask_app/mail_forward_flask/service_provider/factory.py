"""
   service_provider_factory.py
"""
import logging
from mail_forward_flask.service_provider.mandrill import Mandrill
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
        self._mandrill_api_key = None
        self._default_provider = "mailgun"
        self._logger = logging.getLogger(APP_LOGNAME)

    def set_default_noop(self):
        """
            Set the default servide provider to noop
        """
        self._logger.info("Default provider set to noop")
        self._default_provider = "noop"

    def set_default_mailgun(self):
        """
            Set the default servide provider to mailgun
        """
        self._logger.info("Default provider set to mailgun")
        self._default_provider = "mailgun"

    def set_default_mandrill(self):
        """
            Set the default servide provider to mandrill
        """
        self._logger.info("Default provider set to mandrill")
        self._default_provider = "mandrill"

    def configure_mailgun(self, api_key, domain):
        """
            Sets configuration info needed to
            instantiate Mailgun instance
        """
        self._logger.debug("Configuring mailgun api_key %s... domain %s...",
                           api_key[:5], domain[:5])
        self._mailgun_api_key = api_key
        self._mailgun_domain = domain

    def configure_mandrill(self, api_key):
        """
            Sets configuration info needed to
            instantiate Mandrill instance
        """
        self._logger.debug("Configuring mandril with api_key %s...", api_key[:6])
        self._mandrill_api_key = api_key

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

    def build_mandrill(self):
        """
            Builds and returns Mandrill
            service provider

            raises ServiceProviderFactoryException
            if it is not configured fully
        """
        self._logger.info("Building Mandrill Service Provider")
        if self._mandrill_api_key:
            return Mandrill(api_key=self._mandrill_api_key)

        message = "Mandrill provider not fully configured in Factory"
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
            self._default_provider is noop, mailgun, or mandrill
        """
        if self._default_provider == "noop":
            return self.build_noop()

        if self._default_provider == "mandrill":
            return self.build_mandrill()

        # default to mailgun
        return self.build_mailgun()

# end
