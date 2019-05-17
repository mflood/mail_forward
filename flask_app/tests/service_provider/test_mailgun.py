"""
    test mailgun service provider
"""
import pytest
import requests
import requests_mock
from mail_forward_flask.message_tools.mf_email import MfEmail
from mail_forward_flask.service_provider.mailgun import Mailgun
from mail_forward_flask.service_provider import ServiceProviderException

@pytest.fixture()
def req_mock():
    """
        # info on requests mocking
        # usually requests_mock would be available as fixture
        https://requests-mock.readthedocs.io/en/latest/pytest.html

        # but requests_mock not available as fixture in python 3
        https://github.com/pytest-dev/pytest/issues/2749

        # hence, this fixture
    """
    with requests_mock.Mocker() as m:
        yield m


def test_constructor():
    """
        test creating object
    """
    sp = Mailgun(api_key="hi", domain="bye")


def test_send_message(req_mock):
    """
    """

    mock_response = """
        {
          "id": "<MOCK.1.MOCK@sandbox4c3ae61c920d473d8e9ead8dd265bc92.mock.org>",
          "message": "Queued (MOCK). Thank you."
        }"""

    mg = Mailgun(api_key='passthejam', domain='butter')
    api_url = mg.get_mailgun_api_url()

    # this sets up the maildog api_url with a mock response
    req_mock.post(api_url, text=mock_response)

    mg.concrete_send_message(from_address="tswift",
                             to_address="jumba",
                             subject="jello",
                             text="mix")

def test_404_json_response(req_mock):
    """
    """

    mock_response = """
        {
          "message": "Something went horribly wrong."
        }"""

    mg = Mailgun(api_key='passthejam', domain='butter')
    api_url = mg.get_mailgun_api_url()

    # this sets up the maildog api_url with a mock response
    req_mock.post(api_url, text=mock_response, status_code=404)

    with pytest.raises(ServiceProviderException):

        mg.concrete_send_message(from_address="tswift",
                                 to_address="jumba",
                                 subject="jello",
                                 text="mix")

def test_404_text_response(req_mock):
    """
    """

    mock_response = """The world is ending"""

    mg = Mailgun(api_key='passthejam', domain='butter')
    api_url = mg.get_mailgun_api_url()

    # this sets up the maildog api_url with a mock response
    req_mock.post(api_url, text=mock_response, status_code=404)

    with pytest.raises(ServiceProviderException):

        mg.concrete_send_message(from_address="tswift",
                                 to_address="jumba",
                                 subject="jello",
                                 text="mix")


def test_connection_error(req_mock):
    """
    """

    mock_response = """The world is ending"""

    mg = Mailgun(api_key='passthejam', domain='butter')
    api_url = mg.get_mailgun_api_url()

    # this sets up the maildog api_url with a mock response
    req_mock.post(api_url, exc=requests.exceptions.ConnectionError)

    with pytest.raises(ServiceProviderException):

        mg.concrete_send_message(from_address="tswift",
                                 to_address="jumba",
                                 subject="jello",
                                 text="mix")


def test_invalid_schema(req_mock):
    """
    """

    mock_response = """The world is ending"""

    mg = Mailgun(api_key='passthejam', domain='butter')
    api_url = mg.get_mailgun_api_url()

    # this sets up the maildog api_url with a mock response
    req_mock.post(api_url, exc=requests.exceptions.InvalidSchema)

    with pytest.raises(ServiceProviderException):

        mg.concrete_send_message(from_address="tswift",
                                 to_address="jumba",
                                 subject="jello",
                                 text="mix")


