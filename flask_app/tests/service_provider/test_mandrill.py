"""
    test mandrill service provider
"""
import pytest
import requests
import requests_mock
from mail_forward_flask.message_tools.mf_email import MfEmail
from mail_forward_flask.service_provider.mandrill import Mandrill
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
    sp = Mandrill(api_key="hi")


def test_send_message(req_mock):
    """
    """

    mock_response = """
        [
            {
                "email": "recipient.email@example.com",
                "status": "queued",
                "_id": "42461e9aa82a4871a0c9a1fab2d5bb6c",
                "reject_reason": null
            }
        ]
        """

    mg = Mandrill(api_key='passthejam')
    api_url = mg.get_mandrill_api_url()

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
            "status": "error",
            "code": -2,
            "name": "ValidationError",
            "message": "Validation error: {\"message\":{\"from_email\":\"An email address must contain a single @\"}}"
        }
        """

    mg = Mandrill(api_key='passthejam')
    api_url = mg.get_mandrill_api_url()

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

    mg = Mandrill(api_key='passthejam')
    api_url = mg.get_mandrill_api_url()

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

    mg = Mandrill(api_key='passthejam')
    api_url = mg.get_mandrill_api_url()

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

    mg = Mandrill(api_key='passthejam')
    api_url = mg.get_mandrill_api_url()

    # this sets up the maildog api_url with a mock response
    req_mock.post(api_url, exc=requests.exceptions.InvalidSchema)

    with pytest.raises(ServiceProviderException):

        mg.concrete_send_message(from_address="tswift",
                                 to_address="jumba",
                                 subject="jello",
                                 text="mix")

def test_str():
    """
        test __str__
    """
    mg = Mandrill(api_key='whatever')
    assert(str(mg) == "mandrill")
