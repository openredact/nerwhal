from abc import ABC, abstractmethod


class Recognizer(ABC):
    @classmethod
    @abstractmethod
    def BACKEND(cls):
        pass

    @classmethod
    @abstractmethod
    def TAG(cls):
        pass

    @classmethod
    @abstractmethod
    def SCORE(cls):
        """A confidence score that estimates the probability that a result of this recognizer is a
        named entity for its tag."""
        pass
