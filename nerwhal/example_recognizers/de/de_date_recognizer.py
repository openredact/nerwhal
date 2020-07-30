from nerwhal.recognizer_bases.entity_ruler_recognizer import EntityRulerRecognizer


class DeDateRecognizer(EntityRulerRecognizer):
    """
    """

    TAG = "DATE"
    SCORE = 0.99
    CONTEXT_WORDS = ["Datum", "Tag", "Geburtstag", "Geburtsdatum"]

    @property
    def patterns(self):
        return [
            [  # DIN 1355-1, e.g. 24.12.2020
                {"TEXT": {"REGEX": r"^(0?[1-9]|[1-2][0-9]|3[01])\.(0?[1-9]|1[0-2])\.[1-2]?[0-9]?[0-9][0-9]$"}},
            ],
            [  # DIN 5008, e.g. 2020-12-24
                {"TEXT": {"REGEX": r"^[1-2][0-9]{3}$"}},
                {"TEXT": "-"},
                {"TEXT": {"REGEX": r"^(0[1-9]|1[0-2])$"}},
                {"TEXT": "-"},
                {"TEXT": {"REGEX": r"^(0[1-9]|[1-2][0-9]|3[01])$"}},
            ],  # Written out, e.g. 24. Aug. 2020, optional with day Mittwoch, 24. Aug. 2020
            [
                {"TEXT": {"REGEX": r"^Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag"}, "OP": "?"},
                {"IS_ALPHA": False, "OP": "?"},
                {"TEXT": {"REGEX": r"^(0?[1-9]|[1-2][0-9]|3[01])\.$"}},
                {"TEXT": {"REGEX": r"^Jan|Feb|Mrz|Mä|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez"}},
                {"TEXT": {"REGEX": r"^([1-2][0-9]{3}|[1-9][0-9]{2}|[0-9]{2})$"}},
            ],
        ]
