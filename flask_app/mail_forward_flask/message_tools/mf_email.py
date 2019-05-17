"""
    Object represents the Mail Forward email information
    that will be collected and sent

    provides
     - validation
     - loading from dictionardictionary
"""
import logging
from mail_forward_flask.loggingsetup import APP_LOGNAME
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
        self._logger = logging.getLogger(APP_LOGNAME)

    def load_from_dict(self, dictionary):
        """
            Loads member variables from dictionary
        """
        self._logger.debug("load_from_dict is type: %s", type(dictionary))
        assert isinstance(dictionary, dict)

        self._to_address = dictionary.get("to", "").strip()
        self._to_name = dictionary.get("to_name", "").strip()
        self._from_address = dictionary.get("from", "").strip()
        self._from_name = dictionary.get("from_name", "").strip()
        self._subject = dictionary.get("subject", "").strip()
        self._body = dictionary.get("body", "").strip()

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
