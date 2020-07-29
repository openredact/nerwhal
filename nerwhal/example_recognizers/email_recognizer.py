import re

from nerwhal.recognizer_bases.re_recognizer import ReRecognizer


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

    TAG = "EMAIL"
    SCORE = 0.95
    FLAGS = re.VERBOSE

    @property
    def regexp(self):
        return r""" [a-zA-Z0-9!#$%&'"*+\-/=?^_`{|}~]  # the first character cannot be a .
                   ([a-zA-Z0-9!#$%&'"*+\-/=?^_`{|}~\.]*)  # local part
                   @
                   ((?!-)[a-zA-Z0-9\-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}  # domain part)"""
