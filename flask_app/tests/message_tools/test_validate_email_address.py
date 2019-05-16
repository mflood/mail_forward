
import pytest
from mail_forward_flask.message_tools import InvalidEmailException
from mail_forward_flask.message_tools import validate_email_address


def test_bad_emails():
    with pytest.raises(InvalidEmailException):
        validate_email_address("Mr. Fake")
    with pytest.raises(InvalidEmailException):
        validate_email_address("I am a dog")
    with pytest.raises(InvalidEmailException):
        validate_email_address("too@many@ats.com")
    with pytest.raises(InvalidEmailException):
        validate_email_address("")
    with pytest.raises(InvalidEmailException):
        validate_email_address(None)

def test_good_emails():
    validate_email_address("noreply@mybrightwheel.com")
    validate_email_address("fake@example.com")
