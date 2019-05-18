"""
    mailgun.py
"""
import logging
from json.decoder import JSONDecodeError
import requests
from mail_forward_flask.loggingsetup import APP_LOGNAME
from mail_forward_flask.service_provider import ServiceProvider
from mail_forward_flask.service_provider import ServiceProviderException

class Mailgun(ServiceProvider):
    """
        Concrete implementation of ServiceProvider
        sends mail through mailgun
    """

    def __init__(self, api_key, domain):

        super(Mailgun, self).__init__()

        self._logger = logging.getLogger(APP_LOGNAME)
        self._api_key = api_key
        self._domain = domain

    def __str__(self):
        return "mailgun"

    def get_mailgun_api_url(self):
        """
            Returns the URL use to hit the api
            allows us to mock the url in testing
        """
        return "https://api.mailgun.net/v3/{}/messages".format(self._domain)

    def concrete_send_message(self, mf_email):
        """
            Send message using mailgun API
            This is called by base class when send_message(mf_email) is invoked
            Throws ServiceProviderException if the api call fails
        """
        try:
            response = requests.post(
                self.get_mailgun_api_url(),
                auth=("api", self._api_key),
                data={"from": mf_email.get_full_address_from(),
                      "to": [mf_email.get_full_address_to()],
                      "subject": mf_email.get_subject(),
                      "text": mf_email.get_text})

        except requests.exceptions.ConnectionError as error:
            self._logger.error(error)
            raise ServiceProviderException(error)

        except requests.exceptions.InvalidSchema as error:
            self._logger.error(error)
            raise ServiceProviderException(error)

        self._logger.debug("dir response: %s", dir(response))
        self._logger.debug("response.raw: %s", response.raw)
        self._logger.debug("response.text: %s", response.text)
        self._logger.debug("response.headers: %s", response.headers)
        self._logger.debug("response.status_code: %s", response.status_code)

        if response.status_code == 200:
            mailgun_id = response.json()["id"]
            mailgun_message = response.json()["message"]
            self._logger.info("Sent mailgun message. %s: %s", mailgun_id, mailgun_message)

        else:
            try:
                # if there is json, they provide a message
                mailgun_message = response.json()["message"]
            except JSONDecodeError:
                # otherwise just grab text
                mailgun_message = response.text

            error_message = ("Code {} Failed to send mailgun message: "
                             "{}".format(response.status_code, mailgun_message))
            self._logger.error(error_message)
            raise ServiceProviderException(error_message)

# pylint: disable=invalid-name
# pylint: disable=protected-access
if __name__ == "__main__":
    #    Invoke directly for integration Test
    #    In bash:
    #
    #    export MAILGUN_API_KEY='YOUR_API_KEY'
    #    export MAILGUN_DOMAIN='YOUR_DOMAIN'

    import os                                                     # pragma: no cover
    from mail_forward_flask.message_tools.mf_email import MfEmail # pragma: no cover

    info_dict = {                                                 # pragma: no cover
        "from_name": "Fox",                                       # pragma: no cover
        "from_address": "hermannwest@gmail.com",                  # pragma: no cover
        "to_name": "Tom",                                         # pragma: no cover
        "to_address": "hermannwest@gmail.com",                    # pragma: no cover
        "subject": "You won't believe what's in this email",      # pragma: no cover
        "text": "<b>Bold Content</b>"                             # pragma: no cover
    }                                                             # pragma: no cover

    email = MfEmail()                                             # pragma: no cover
    email.load_from_dict(dictionary=info_dict)                    # pragma: no cover
    mg = Mailgun(api_key=os.environ["MF_MAILGUN_API_KEY"],        # pragma: no cover
                 domain=os.environ["MF_MAILGUN_DOMAIN"])          # pragma: no cover
    mg.concrete_send_message(mf_email=email)                      # pragma: no cover
# end
