from abc import abstractmethod

from .base import Recognizer


class ReRecognizer(Recognizer):
    """The base class for all regular expression based recognizers."""

    BACKEND = "re"
    GROUP = 0  # the name or number of the capture group, if it is 0 the whole match will be taken
    FLAGS = 0  # re compiler flags, e.g. re.VERBOSE

    @property
    @abstractmethod
    def regexp(self):
        """A string that describes the regular expression pattern for this recognizer."""
        pass
