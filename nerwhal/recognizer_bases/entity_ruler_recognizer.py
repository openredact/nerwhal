from abc import abstractmethod

from .base import Recognizer


class EntityRulerRecognizer(Recognizer):
    BACKEND = "entity-ruler"

    @property
    @abstractmethod
    def patterns(self):
        pass
