from abc import ABC, abstractmethod

_recognizer_classes = ()
__all__ = [recognizer.__name__ for recognizer in _recognizer_classes]
__tags__ = set([tag for recognizer in _recognizer_classes for tag in recognizer.TAGS])


class Recognizer(ABC):
    @property
    @abstractmethod
    def backend(self):
        pass

    @property
    @abstractmethod
    def precision(self):
        """The confidence that a match is of the respective entity."""
        pass

    @property
    @abstractmethod
    def entity(self):
        pass
