from abc import abstractmethod

from .base import Recognizer


class EntityRulerRecognizer(Recognizer):
    """The base class for all spaCy EntityRuler based recognizers."""

    BACKEND = "entity-ruler"

    @property
    @abstractmethod
    def patterns(self):
        """This property returns the patterns for the entity ruler.

        See https://spacy.io/usage/rule-based-matching#entityruler for more information on the patterns and
        https://spacy.io/api/token#attributes for the available token attributes.
        """
        pass
