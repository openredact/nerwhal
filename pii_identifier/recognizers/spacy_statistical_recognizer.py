from pii_identifier.recognizers._recognizer_base import Recognizer


class SpacyStatisticalRecognizer(Recognizer):
    """Recognize named entities using the spaCy statistical model."""

    @property
    def backend(self):
        return "spacy"
