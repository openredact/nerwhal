from nerwhal.recognizer_bases.entity_ruler_recognizer import EntityRulerRecognizer


class MoneyRecognizer(EntityRulerRecognizer):
    """This recognizes money amounts written with a currency symbols. Currency codes or names are not recognized.
    """

    TAG = "MONEY"
    SCORE = 0.99

    @property
    def patterns(self):
        return [
            [{"TEXT": {"REGEX": r"^\d[,\.\d]+\d$"}}, {"IS_CURRENCY": True}],
            [{"IS_CURRENCY": True}, {"TEXT": {"REGEX": r"^\d[,\.\d]+\d$"}}],
        ]
