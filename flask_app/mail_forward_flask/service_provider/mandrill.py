"""
    mandrill.py
"""
import logging
import json
from json.decoder import JSONDecodeError
import requests
from mail_forward_flask.loggingsetup import APP_LOGNAME
from mail_forward_flask.service_provider import ServiceProvider
from mail_forward_flask.service_provider import ServiceProviderException

class Mandrill(ServiceProvider):
    """
        Concrete implementation of ServiceProvider
        sends mail through mandrill
    """

    def __init__(self, api_key):

        super(Mandrill, self).__init__()

        self._logger = logging.getLogger(APP_LOGNAME)
        self._api_key = api_key

    def __str__(self):
        return "mandrill"

    # pylint: disable=no-self-use
    def get_mandrill_api_url(self):
        """
            Returns the URL use to hit the api
            allows us to mock the url in testing
        """
        return "https://mandrillapp.com/api/1.0/messages/send.json"

    def concrete_send_message(self, from_address, to_address, subject, text):
        """
            Send message using mandrill API
            This is called by base class when send_message(mf_email) is invoked
            Throws ServiceProviderException if the api call fails

curl -A  'Mandrill-Curl/1.0' -d '{
    "key": "API-KEY",
    "message": {
        "text": "Example text content",
        "subject": "example subject",
        "from_email": "message.from_email@example.com",
        "from_name": "Example Name",
        "to": [
            {
                "email": "recipient.email@example.com",
                "name": "Recipient Name",
                "type": "to"
            }
        ]
    }
        """

        try:
            response = requests.post(
                self.get_mandrill_api_url(),
                data=json.dumps({"key": self._api_key,
                                 "message": {
                                     "text": text,
                                     "subject": subject,
                                     "from_email": "hermannwest@gmail.com",
                                     "from_name": "matt",
                                     "to": [{
                                         "email": "Bill",
                                         "name": "hermannwest@gmail.com",
                                         "type": "to"
                                     }],}}))

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
            mandrill_id = response.json()[0]["_id"]
            mandrill_status = response.json()[0]["status"]

            if response.json()[0]["status"] == "invalid":
                error_message = ("Code {} Failed to send mandrill message: "
                                 "{}".format(response.status_code, mandrill_status))
                self._logger.error(error_message)
                raise ServiceProviderException(error_message)
            else:
                self._logger.info("Sent mandrill message. %s: %s", mandrill_id, mandrill_status)

        else:
            try:
                # if there is json, they provide a message
                mandrill_message = response.json()["message"]
            except JSONDecodeError:
                # otherwise just grab text
                mandrill_message = response.text

            error_message = ("Code {} Failed to send mandrill message: "
                             "{}".format(response.status_code, mandrill_message))
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
    import os                                                       # pragma: no cover
    mg = Mandrill(api_key=os.environ["MF_MANDRILL_API_KEY"])        # pragma: no cover
    mg.concrete_send_message(from_address="hermannwest@gmail.com",  # pragma: no cover
                             to_address="hermannwest@gmail.com",    # pragma: no cover
                             subject="my test",                     # pragma: no cover
                             text="hi there.")                      # pragma: no cover
# end
