from abc import abstractmethod

from .base import Recognizer


class EntityRulerRecognizer(Recognizer):
    BACKEND = "entity-ruler"

    def __init__(self, nlp):
        self.nlp = nlp

    @property
    @abstractmethod
    def patterns(self):
        pass
