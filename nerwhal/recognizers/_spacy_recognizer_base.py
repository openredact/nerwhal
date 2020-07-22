from abc import abstractmethod

from nerwhal.recognizers._recognizer_base import Recognizer


class SpacyEntityRulerRecognizer(Recognizer):
    @property
    def backend(self):
        return "spacy"

    @property
    @abstractmethod
    def rules(self):
        pass

    def _create_rules(self, patterns, label):
        return [{"label": label, "pattern": pattern} for pattern in patterns]
