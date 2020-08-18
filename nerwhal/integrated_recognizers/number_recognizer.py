from nerwhal.recognizer_bases.re_recognizer import ReRecognizer


class NumberRecognizer(ReRecognizer):
    """Recognize anything that is a number.

    This recognizer searches for digits, that might be separated by commas or dots. Having a low score, it can be used as a
    fallback to catch any number that hasn't been recognized by a more specific recognizer.
    """

    TAG = "NUMBER"
    SCORE = 0.5  # give it a low score so that it doesn't overwrite other entities

    @property
    def regexp(self):
        return r"\d[,\.\d]*\d?"
