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
        """This is the estimated confidence that a found match is of the respective entity.

        Precision == How many found elements are relevant

        Note that the score is always a rough estimate, which might be totally off.
        Exact scores can only be computed on the data with gold annotations."""
        pass
