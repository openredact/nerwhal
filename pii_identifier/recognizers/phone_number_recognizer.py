from pii_identifier.recognizers._spacy_recognizer_base import SpacyEntityRulerRecognizer


class PhoneNumberRecognizer(SpacyEntityRulerRecognizer):
    # TODO WIP
    pattern = [
        {
            "label": "PHONE",
            "pattern": [
                {"TEXT": {"REGEX": r"^\+\d{1,3}$"}},
                {"ORTH": "(", "OP": "?"},
                {"IS_DIGIT": True},
                {"ORTH": ")", "OP": "?"},
                {"SHAPE": "dddd", "LENGTH": {"<=": 6}},
            ],
        }
    ]

    @property
    def patterns(self):
        return self.pattern
