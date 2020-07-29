from abc import abstractmethod

from .base import Recognizer


class ReRecognizer(Recognizer):
    BACKEND = "re"

    @property
    @abstractmethod
    def FLAGS(self):
        pass

    @property
    @abstractmethod
    def regexp(self):
        pass
