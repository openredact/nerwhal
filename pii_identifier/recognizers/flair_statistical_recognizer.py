from pii_identifier.recognizers._recognizer_base import Recognizer


class FlairStatisticalRecognizer(Recognizer):
    """Recognize named entities using the flair statistical model."""

    @property
    def backend(self):
        return "flair"
