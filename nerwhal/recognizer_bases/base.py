from abc import ABC, abstractmethod


class Recognizer(ABC):
    """This interface is the base class for all recognizers.

    Recognizers are basically configurations for the backends. Each backend runs one or more recognizers to search for
    entities.

    For efficiency reasons do the heavy lifting of loading files or expensive computations in the `__init__` method instead of
    in the properties. The recognizer is only initialized once, but the properties are called on every run.
    """

    CONTEXT_WORDS = []

    @property
    @abstractmethod
    def BACKEND(self):
        """The backend that this recognizer operates with."""
        pass

    @property
    @abstractmethod
    def TAG(self):
        """The recognizer finds named entities for this tag."""
        pass

    @property
    @abstractmethod
    def SCORE(self):
        """The confidence score for a result of this recognizer being a named entity for its tag, i.e. the precision of this
        recognizer."""
        pass
