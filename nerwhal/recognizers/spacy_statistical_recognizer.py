from nerwhal.recognizers._recognizer_base import Recognizer


class SpacyStatisticalRecognizer(Recognizer):
    """Recognize named entities using the spaCy statistical model."""

    TAGS = ["PER", "LOC", "ORG", "MISC"]  # TODO this actually depends on the loaded model

    @property
    def backend(self):
        return "spacy"
