from abc import ABC, abstractmethod


class Recognizer(ABC):
    @property
    @abstractmethod
    def backend(self):
        pass
