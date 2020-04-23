from abc import abstractmethod

from pii_identifier.recognizers._recognizer_base import Recognizer


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
        """The estimated confidence that a match is of the respective entity."""
        pass
