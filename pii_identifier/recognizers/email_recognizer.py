from pii_identifier.recognizers._re_recognizer_base import ReRecognizer


class EmailRecognizer(ReRecognizer):
    @property
    def regexp(self):
        # TODO add support for
        #  - IP address domains
        #  - domain names without TLD
        #  - UTF8 characters in local and domain part
        #  - special characters inside quoted strings
        #  - don't accept . as first character

        # TODO should we enforce a space or other character before the e-mail? how to handle e.g. a@b@c@example.com

        # to also recognize addresses with syntax errors this does purposefully not implement
        # all constraints of the e-mail specification
        return r"""([a-zA-Z0-9!#$%&'*+-/=?^_`{|}~\.]+)  # local part
                   @
                   ((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}  # domain part)"""

    @property
    def entity(self):
        return "EMAIL"

    @property
    def precision(self):
        return 1.0
