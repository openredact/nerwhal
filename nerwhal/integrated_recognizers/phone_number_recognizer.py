import re

from nerwhal.recognizer_bases.re_recognizer import ReRecognizer


class PhoneNumberRecognizer(ReRecognizer):
    """Recognize phone numbers that follow several common German national and international patterns.

    This recognizer aims at finding numbers of DIN 5008 and E.123 style, Microsoft's canonical number format, and some
    non-standard but frequently used styles. Because of the freedom that a user has in writing a phone number and splitting it
    into differently sized blocks, it is difficult to find all occurrences and to not produce too many false positives.
    You can refer to the regular expression below or the tests to see what sequences are detected.

    Consider the following remarks and limitations:
    - as there are many ways in which a phone number can be formatted, we cannot match all of them
    - making the patterns too universal may produce false positives for other sequences of digits such as credit card numbers
    - choosing the quantifiers for the digits in a black constitutes a trade-off between detecting more phone numbers in
      less common formats vs producing false positives
    - especially, numbers in foreign styles or numbers in German style that represent a foreign number aren't tested and may
      not be recognized
    """

    TAG = "PHONE"
    SCORE = 0.8
    GROUP = 1
    FLAGS = re.VERBOSE
    CONTEXT_WORDS = ["number", "Nummer", "tel.", "Tel.", "mobil", "Telefon", "telephone"]

    COUNTRY_CODE_REGEX = r"\(?(\+|00)\)?\d{1,3}"
    AREA_CODE = r"(\(?0\)?[ ]?\d{1,4}|\(?\d{1,5}\)?)"
    BASE_NUMBER = r"\d{1,4}[ -]?\d{1,4}[ -]?\d{1,2}"
    EXTENSION = r"([ ]?-[ ]?\d{1,3}|[ ]\d{0,3}[ ]?\/[ ]?\d{1,3})"

    @property
    def regexp(self):
        return rf"""# there should not be a digit in the preceding two characters and no dot directly before a number
                    (?:^|^[^\.\d]|[^\d][^\.\d])
                    (  # the number will be in the matching group 1
                    # >>> International numbers
                    # Microsoft's canonical format, e.g. +49 (030) 12345, +49 (0) 30 12345
                    # E.123 style with blocks, e.g. +22 607 123 4567
                    # Abbreviated, e.g. tel:+49-30-1234567
                    ({self.COUNTRY_CODE_REGEX}[ \.\-]?)?
                    # >>> National numbers
                    # DIN 5008, e.g. 030 12345-67
                    # E.123, e.g. (030) 12345 0 / 67
                    # Non-standard format, e.g. 0 30 / 12 34 56
                    {self.AREA_CODE}([ -]|([ ]?\/[ ]?))?{self.BASE_NUMBER}{self.EXTENSION}?
                    )
                    # the following two characters should not be digits
                    (?:$|[^\d]$|[^\d][^\d])
                    """
