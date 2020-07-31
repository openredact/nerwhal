from abc import abstractmethod

from .base import Recognizer


class FlashtextRecognizer(Recognizer):
    BACKEND = "flashtext"

    @property
    @abstractmethod
    def keywords(self):
        pass
