from abc import abstractmethod

from nerwhal.recognizer_bases import Recognizer


class SpacyPipeComponent(Recognizer):
    @property
    def backend(self):
        return "spacy"


class SpacyEntityRulerRecognizer(SpacyPipeComponent):
    @property
    @abstractmethod
    def patterns(self):
        pass
