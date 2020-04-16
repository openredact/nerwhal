from pii_identifier.recognizers._recognizer_base import Recognizer


class FlairStatisticalRecognizer(Recognizer):
    @property
    def backend(self):
        return "flair"
