"""
    test noop service provider
"""
import pytest
from mail_forward_flask.message_tools.mf_email import MfEmail
from mail_forward_flask.service_provider.noop import Noop

def test_constructor():
    """
        test creating object
    """
    sp = Noop()

def test_send_message():
    """
        calls noop send_message
    """
    sp = Noop()
    sp = sp.send_message(mf_email=MfEmail())


