from abc import abstractmethod

from nerwhal.recognizers.recognizer_base import Recognizer


class ReRecognizer(Recognizer):
    @property
    def backend(self):
        return "re"

    @property
    @abstractmethod
    def regexp(self):
        pass

    @property
    @abstractmethod
    def entity(self):
        pass

    @property
    @abstractmethod
    def precision(self):
        """The confidence that a match is of the respective entity."""
        pass
