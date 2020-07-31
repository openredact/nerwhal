from abc import ABC, abstractmethod
from typing import Type

from nerwhal.recognizer_bases.base import Recognizer


class Backend(ABC):
    """Backends are the engines behind the recognizers that drive the search for named entities.

    Recognizers use the functionality provided by a backend to do their job. Each recognizer has to specify one backend
    that it operates on.
    """

    @abstractmethod
    def register_recognizer(self, recognizer_cls: Type[Recognizer]):
        """Add the given recognizer to this backend instance.

        One backend can have several recognizers. Once added they cannot be removed anymore.
        To remove them create a new backend instance.
        """
        pass

    @abstractmethod
    def run(self, text):
        """Run the backend and all registered recognizers.

        :return: the list of named entities that have been identified
        """
        pass
