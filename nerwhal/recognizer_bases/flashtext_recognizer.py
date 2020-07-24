from abc import abstractmethod

from nerwhal.recognizer_bases import Recognizer


class FlashtextRecognizer(Recognizer):
    @property
    def backend(self):
        return "flashtext"

    @property
    @abstractmethod
    def keywords(self):
        pass
