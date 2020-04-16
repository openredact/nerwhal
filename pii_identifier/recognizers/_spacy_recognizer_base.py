from abc import abstractmethod

from pii_identifier.recognizers._recognizer_base import Recognizer


class SpacyEntityRulerRecognizer(Recognizer):
    @property
    def backend(self):
        return "spacy"

    @property
    @abstractmethod
    def patterns(self):
        pass
