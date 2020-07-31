from nerwhal.recognizer_bases.re_recognizer import ReRecognizer


class CardinalRecognizer(ReRecognizer):
    """
    """

    TAG = "CARDINAL"
    SCORE = 0.95

    @property
    def regexp(self):
        return r"\d[,\.\d]+\d"
