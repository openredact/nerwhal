from nerwhal.recognizer_bases.entity_ruler_recognizer import EntityRulerRecognizer


class MoneyRecognizer(EntityRulerRecognizer):
    """Recognize money amounts written as a number followed by a currency symbol.

    Attention: This recognizer does only match one of the manifold ways that money amounts can be written.

    For example, currency codes or currency names are not recognized.
    """

    TAG = "MONEY"
    SCORE = 0.99

    @property
    def patterns(self):
        return [
            [{"TEXT": {"REGEX": r"^\d[,\.\d]+\d$"}}, {"IS_CURRENCY": True}],
            [{"IS_CURRENCY": True}, {"TEXT": {"REGEX": r"^\d[,\.\d]+\d$"}}],
        ]
