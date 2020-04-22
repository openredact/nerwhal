from pii_identifier.recognizers._spacy_recognizer_base import SpacyEntityRulerRecognizer


class PhoneNumberRecognizer(SpacyEntityRulerRecognizer):
    """
    Note that this is by no means exhaustive or precise, as there are so many different ways to write a phone number.
    """

    COUNTRY_CODES_REGEX = r"^(\+|[00])\d{1,4}$"
    MAX_LEN_AREA_CODE = 5
    MAX_LEN_SUBSCRIBER_NUMBER = 8
    MAX_LEN_EXTENSION = 3
    MAX_LEN_BLOCK = 4  # the maximum length of space separated blocks (123456789 => 1234 5678 9)

    phone_patterns = [
        # >>> International numbers
        [  # Microsoft's canonical format, e.g. +49 (030) 12345
            {"TEXT": {"REGEX": COUNTRY_CODES_REGEX}},
            {"TEXT": "(", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_AREA_CODE}},
            {"TEXT": ")", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_SUBSCRIBER_NUMBER}},
            {"TEXT": "-", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_EXTENSION}, "OP": "?"},
        ],
        [  # Microsoft's canonical format, e.g. +49 (0) 30 12345
            {"TEXT": {"REGEX": COUNTRY_CODES_REGEX}},
            {"TEXT": "(", "OP": "?"},
            {"TEXT": "0"},
            {"TEXT": ")", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_AREA_CODE - 1}},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_SUBSCRIBER_NUMBER}},
            {"TEXT": "-", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_EXTENSION}, "OP": "?"},
        ],
        [  # E.123 style with blocks
            {"TEXT": {"REGEX": COUNTRY_CODES_REGEX}},
            {"IS_SPACE": True, "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_AREA_CODE}},
            {"IS_SPACE": True, "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_BLOCK}, "OP": "?"},
            {"IS_SPACE": True, "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_BLOCK}, "OP": "?"},
            {"IS_SPACE": True, "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": max(MAX_LEN_BLOCK, MAX_LEN_EXTENSION)}, "OP": "?"},
            {"TEXT": "/", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_EXTENSION}, "OP": "?"},
        ],
        [  # Abbreviated, e.g. tel:+49-30-1234567
            {"TEXT": {"REGEX": COUNTRY_CODES_REGEX.replace("^", r"^\w+\.?:")}},
            {"TEXT": {"IN": [" ", "-"]}},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_AREA_CODE}},
            {"TEXT": {"IN": [" ", "-"]}},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_SUBSCRIBER_NUMBER}},
            {"TEXT": {"IN": [" ", "-"]}, "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_EXTENSION}, "OP": "?"},
        ],
        [{"TEXT": {"REGEX": COUNTRY_CODES_REGEX.replace("$", r"(\.\d{2,14})+$")}}],  # Dotted format, e.g. +49.3012345
        # >>> National numbers
        [  # DIN 5008, e.g. 030 12345-67
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_AREA_CODE}},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_SUBSCRIBER_NUMBER}},
            {"TEXT": "-", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_EXTENSION}, "OP": "?"},
        ],
        [  # E.123, e.g. (030) 12345 0 / 67
            {"TEXT": "(", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_AREA_CODE}},
            {"TEXT": ")", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_SUBSCRIBER_NUMBER}},
            {"IS_SPACE": True, "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_BLOCK}, "OP": "?"},  # supports max 3 blocks incl. extension
            {"IS_SPACE": True, "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_EXTENSION}, "OP": "?"},
            {"TEXT": "/", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_EXTENSION}, "OP": "?"},  # supports one alternative extension
        ],
        [  # Non-standard format, e.g. 0 30 / 12 34 56
            {"TEXT": "0", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_AREA_CODE}},
            {"TEXT": "/"},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_BLOCK}},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_BLOCK}},
            {"IS_DIGIT": True, "LENGTH": {"<=": MAX_LEN_BLOCK}},
        ],
    ]

    @property
    def patterns(self):
        return self._add_label(self.phone_patterns, "PHONE")
