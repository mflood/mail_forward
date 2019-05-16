"""
    Object represents the Mail Forward email information
    that will be collected and sent

    provides
     - validation
     - loading from json message
"""
import json
from json.decoder import JSONDecodeError
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

class MfEmail():
    """
        Represents Email to be Forward
    """

    def __init__(self):
        self._to = None
        self._to_name = None
        self._from = None
        self._from_name = None
        self._subject = None
        self._body = None

    def load_from_json(self, json_string):
        """
            Loads member variables from json string
        """
        try:
            as_object = json.loads(json_string)
            self._to = as_object.get("to")
            self._to_name = as_object.get("to_name")
            self._from = as_object.get("from")
            self._from_name = as_object.get("from_name")
            self._subject = as_object.get("subject")
            self._body = as_object.get("body")
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
        required_fields = [(self._to, 'to'),
                           (self._to_name, 'to_name'),
                           (self._from, 'from'),
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

    def as_dict(self):
        """
            Getter for all member variables
        """
        return {
            'to': self._to,
            'to_name': self._to_name,
            'from': self._from,
            'from_name': self._from_name,
            'subject': self._subject,
            'body': self._body,
        }

# end
