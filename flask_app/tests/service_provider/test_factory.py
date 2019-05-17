"""
    test service provider factory
"""
import pytest
import requests
import requests_mock
from mail_forward_flask.service_provider.mailgun import Mailgun
from mail_forward_flask.service_provider.noop import Noop
from mail_forward_flask.service_provider.factory import ServiceProviderFactory
from mail_forward_flask.service_provider.factory import ServiceProviderFactoryException

def test_constructor():
    """
        test creating object
    """
    spf = ServiceProviderFactory()

def test_noop():
    """
        test factory methods related to noop
    """
    spf = ServiceProviderFactory()
    spf.set_default_noop()
    service_provider = spf.build_default()
    assert isinstance(service_provider, Noop)

def test_mailgun():
    """
        test factory methods related to noop
    """
    spf = ServiceProviderFactory()
    spf.configure_mailgun(api_key="mykey", domain="mydomain")
    spf.set_default_mailgun()
    service_provider = spf.build_default()
    assert isinstance(service_provider, Mailgun)

def test_unconfigured_mailgun():
    """
        test factory methods related to noop
    """
    spf = ServiceProviderFactory()
    spf.set_default_mailgun()
    with pytest.raises(ServiceProviderFactoryException):
        service_provider = spf.build_default()
