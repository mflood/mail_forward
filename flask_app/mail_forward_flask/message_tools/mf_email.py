"""
    Object represents the Mail Forward email information
    that will be collected and sent

    provides
     - validation
     - loading from json message
"""
import json
from json.decoder import JSONDecodeError
from mail_forward_flask.message_tools import convert_html_to_text
from mail_forward_flask.message_tools import validate_email_address
from mail_forward_flask.message_tools import InvalidEmailException


class InvalidMfEmailException(Exception):
    """
        Raised when email is found to be invalid
        Takes a list of things that are wrong with
        the email

        except InvalidMfEmailException as error:
            email_errors = error.email_errors
    """
    def __init__(self, message, email_errors):
        super(InvalidMfEmailException, self).__init__(message)
        self.error_list = email_errors


def make_email_address(name, address):
    """
        Given a name like 'Bob'
        and an address like 'bob@example.com'
        returns "Bob <bob@example.com>"
    """

    # if email address is already
    # wrapped in angle brackets, remove them
    if address:
        address = address.strip('<>')
        address = address.strip()
    else:
        # we don't want "None" ending up as the email
        address = ""

    if name:
        name = name.strip()
    else:
        # we don't want "None" ending up as the name
        name = ""


    if name and address:
        return "{} <{}>".format(name, address)

    # if no name, just return the stripped email
    return "{}".format(address)

class MfEmail():
    """
        Represents Email to be Forward
    """

    def __init__(self):
        self._to_address = ""
        self._to_name = ""
        self._from_address = ""
        self._from_name = ""
        self._subject = ""
        self._body = ""

    def load_from_json(self, json_string):
        """
            Loads member variables from json string
        """
        try:
            as_object = json.loads(json_string)
            self._to_address = as_object.get("to", "").strip()
            self._to_name = as_object.get("to_name", "").strip()
            self._from_address = as_object.get("from", "").strip()
            self._from_name = as_object.get("from_name", "").strip()
            self._subject = as_object.get("subject", "").strip()
            self._body = as_object.get("body", "").strip()
        except TypeError as error:
            raise InvalidMfEmailException("Could not decode json: {}".format(error), [])
        except JSONDecodeError as error:
            raise InvalidMfEmailException("Could not decode json: {}".format(error), [])

    def validate(self):
        """
            Checks that all fields are populated
            fit their domain
        """

        email_errors = []
        address_fields = ['to', 'from']

        # these fields need to be present and populated in json
        required_fields = [(self._to_address, 'to'),
                           (self._to_name, 'to_name'),
                           (self._from_address, 'from'),
                           (self._from_name, 'from_name'),
                           (self._subject, 'subject'),
                           (self._body, 'body'),
                           ]

        for member_var, fieldname in required_fields:
            if not member_var:
                error_string = "Field '{}' is required".format(fieldname)
                email_errors.append(error_string)
            elif fieldname in address_fields:
                try:
                    validate_email_address(member_var)
                except InvalidEmailException:
                    error_string = "Address supplied for field '{}' is not valid.".format(fieldname)
                    email_errors.append(error_string)

        if email_errors:
            message = "Missing fields"
            raise InvalidMfEmailException(message, email_errors)

    def get_subject(self):
        """
            getter for subject
        """
        return self._subject

    def get_text(self):
        """
            Returns plaintext version of body
        """
        # pseudo detect HTML
        if "<" in self._body and ">" in self._body:
            return convert_html_to_text(self._body)

        return self._body

    def get_full_address_to(self):
        """
            getter for "to" address
            constructs and returns a full email address
            from name and email
        """
        to_address = make_email_address(name=self._to_name,
                                        address=self._to_address)
        return to_address

    def get_full_address_from(self):
        """
            getter for "from" address
            constructs and returns a full email address
            from name and email
        """
        from_address = make_email_address(name=self._from_name,
                                          address=self._from_address)
        return from_address

# end
