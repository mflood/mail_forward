
import pytest
from mail_forward_flask.message_tools.mf_email import InvalidMfEmailException

from mail_forward_flask.message_tools.mf_email import MfEmail



def get_test_json():
    json_string = """
    {
        "to": "fake@example.com",
        "to_name": "Mr. Fake",
        "from": "noreply@mybrightwheel.com", 
        "from_name": "Brightwheel",
        "subject": "A Message from Brightwheel", 
        "body": "<h1>Your Bill</h1><p>$10</p>"
    }
    """
    return json_string



def test_constructor():

    mf_email = MfEmail()

def test_load_from_json():
    mf_email = MfEmail()
    mf_email.load_from_json(json_string=get_test_json())

    as_dict = mf_email.as_dict()
    assert as_dict['to'] == "fake@example.com"
    assert as_dict['to_name'] == "Mr. Fake"
    assert as_dict['from'] == "noreply@mybrightwheel.com"
    assert as_dict['from_name'] == "Brightwheel"
    assert as_dict['subject'] == "A Message from Brightwheel"
    assert as_dict['body'] == "<h1>Your Bill</h1><p>$10</p>"

def test_load_from_json_failure():
    mf_email = MfEmail()
    with pytest.raises(InvalidMfEmailException):
        mf_email.load_from_json(json_string=None)
    with pytest.raises(InvalidMfEmailException):
        mf_email.load_from_json(json_string="hello: af")

def test_validate_success():
    mf_email = MfEmail()
    mf_email.load_from_json(json_string=get_test_json())
    mf_email.validate()

def test_missing_field():
    mf_email = MfEmail()
    json_string = get_test_json()

    # from_name is required, change it to some other name
    json_string = json_string.replace("from_name", "from_gnome")

    mf_email.load_from_json(json_string=json_string)
    with pytest.raises(InvalidMfEmailException):
        mf_email.validate()

def test_invalid_email():
    mf_email = MfEmail()
    json_string = get_test_json()

    # change all '@' signs to '+'
    json_string = json_string.replace("@", "+")

    mf_email.load_from_json(json_string=json_string)
    with pytest.raises(InvalidMfEmailException):
        mf_email.validate()

    try: 
        mf_email.validate()
    except InvalidMfEmailException as mf_error:
        # there should be 2 email address errors
        assert len(mf_error.error_list) == 2

