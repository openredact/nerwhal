from abc import ABC, abstractmethod


class Recognizer(ABC):
    @property
    @abstractmethod
    def BACKEND(self):
        pass

    @property
    @abstractmethod
    def TAG(self):
        pass

    @property
    @abstractmethod
    def SCORE(self):
        """A confidence score that estimates the probability that a result of this recognizer is a
        named entity for its tag."""
        pass
