from nerwhal.recognizers._re_recognizer_base import ReRecognizer


class EmailRecognizer(ReRecognizer):
    """Recognize email addresses.

    Generally this recognizer does not aim at exactly implementing the email syntax specification, but at finding anything
    that looks like an email address - even if it is not compliant.

    Currently not supported are emails with:
    - IP address domains
    - domain names without TLD
    - UTF8 characters in local and domain part
    - special characters inside quoted strings
    """

    TAGS = ["EMAIL"]

    @property
    def regexp(self):
        # TODO don't accept . as first character
        # TODO should we enforce a space or other character before the e-mail? how to handle e.g. a@b@c@example.com
        return r"""([a-zA-Z0-9!#$%&'*+-/=?^_`{|}~\.]+)  # local part
                   @
                   ((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}  # domain part)"""

    @property
    def entity(self):
        return "EMAIL"

    @property
    def precision(self):
        return 1.0
