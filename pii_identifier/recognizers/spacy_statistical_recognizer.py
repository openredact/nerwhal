from pii_identifier.recognizers._recognizer_base import Recognizer


class SpacyStatisticalRecognizer(Recognizer):
    @property
    def backend(self):
        return "spacy"
