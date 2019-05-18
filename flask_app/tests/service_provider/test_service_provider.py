import pytest
from mail_forward_flask.message_tools.mf_email import MfEmail
from mail_forward_flask.service_provider import ServiceProviderException
from mail_forward_flask.service_provider import ServiceProvider

def test_constructor():
    sp = ServiceProvider()

def test_abstract_failure():
    """
        Can't call concrete_send_message
        on abstract class
    """
    sp = ServiceProvider()

    with pytest.raises(ServiceProviderException):
        mf_email = MfEmail()
        sp.send_message(mf_email=mf_email)
        
    #  from_address="test@example.com",
    #  to_address="test@example.com",
    #  subject="Test Sub",
    #    text="Hi There.",

def test_str():
    """
        test __str__
    """
    sp = ServiceProvider()
    assert(str(sp) == "AbstractServiceProvider")

def test_bad_mf_email_arg():
    """
        arg to send_message()
        needs to be a MfEmail object
    """
    sp = ServiceProvider()

    with pytest.raises(AssertionError):
        sp.send_message(mf_email=None)

    with pytest.raises(AssertionError):
        sp.send_message(mf_email="some string")

