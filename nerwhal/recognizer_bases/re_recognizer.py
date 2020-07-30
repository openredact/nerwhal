from abc import abstractmethod

from .base import Recognizer


class ReRecognizer(Recognizer):
    BACKEND = "re"
    GROUP = 0  # the name or number of the capture group, if it is 0 the whole match will be taken
    FLAGS = 0

    @property
    @abstractmethod
    def regexp(self):
        pass
