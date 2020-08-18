import re

from nerwhal.recognizer_bases.re_recognizer import ReRecognizer


class EmailRecognizer(ReRecognizer):
    """Recognize email addresses in the most common formats.

    This recognizer does not aim at exactly implementing the email syntax specification (which is rather complex), but at
    finding a superset of the specification. Thus, it may return results that aren't actually compliant/valid email addresses.

    Also, some addresses that use a less common syntax might be missed. Address syntax features that aren't yet supported
    include but are not limited to:
    - IP address domains
    - domain names without TLD
    - UTF8 characters in local and domain part
    - special characters inside quoted strings
    """

    TAG = "EMAIL"
    SCORE = 0.95
    FLAGS = re.VERBOSE
    CONTEXT_WORDS = ["E-Mail", "email", "Mail", "mail"]

    @property
    def regexp(self):
        return r"""[a-zA-Z0-9!#$%&'"*+\-/=?^_`{|}~]  # the first character cannot be a dot
                   [a-zA-Z0-9!#$%&'"*+\-/=?^_`{|}~\.]*  # local part
                   @
                   ((?!-)[a-zA-Z0-9\-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}  # domain part"""
