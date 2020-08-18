from abc import ABC, abstractmethod
from typing import Type

from nerwhal.recognizer_bases.base import Recognizer


class Backend(ABC):
    """This is the base class for all recognizer backends.

    Backends are the engines behind the recognizers that do the actual hard lifting, i.e. they run the search for named
    entities. Each backend can run several recognizers.
    """

    @abstractmethod
    def register_recognizer(self, recognizer_cls: Type[Recognizer]):
        """Add the given recognizer to this backend instance.

        One backend can have several recognizers. Once a recognizer is added, it cannot be removed (create a new backend
        instance if you have to remove it).
        """
        pass

    @abstractmethod
    def run(self, text):
        """Run the backend using all registered recognizers.

        :return: the list of named entities that have been identified
        """
        pass
