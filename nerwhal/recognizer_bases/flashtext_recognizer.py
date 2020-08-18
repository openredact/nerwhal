from abc import abstractmethod

from .base import Recognizer


class FlashtextRecognizer(Recognizer):
    """The base class for all FlashText based recognizers."""

    BACKEND = "flashtext"

    @property
    @abstractmethod
    def keywords(self):
        """The list of keywords that the FlashText backend is searching for."""
        pass
