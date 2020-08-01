from nerwhal.recognizer_bases.re_recognizer import ReRecognizer


class NumberRecognizer(ReRecognizer):
    """
    """

    TAG = "NUMBER"
    SCORE = 0.5  # give it a low score so that it doesn't overwrite other entities

    @property
    def regexp(self):
        return r"\d[,\.\d]+\d"
