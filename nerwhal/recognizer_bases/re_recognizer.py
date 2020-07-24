import re
from abc import abstractmethod

from nerwhal.recognizer_bases import Recognizer


class ReRecognizer(Recognizer):
    @property
    def backend(self):
        return "re"

    @property
    def flags(self):
        return re.MULTILINE | re.VERBOSE

    @property
    @abstractmethod
    def regexp(self):
        pass
