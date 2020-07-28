import re
from typing import Type

from .base import Backend
from nerwhal.types import NamedEntity
from ..recognizer_bases import ReRecognizer


class ReBackend(Backend):
    def __init__(self):
        self.compiled_regexps = []
        self.entities = []
        self.score = []

    def register_recognizer(self, recognizer_cls: Type[ReRecognizer]):
        recognizer = recognizer_cls()

        self.compiled_regexps += [re.compile(recognizer.regexp, flags=recognizer.flags)]
        self.entities.append(recognizer.TAG)
        self.score.append(recognizer.SCORE)

    def run(self, text):
        ents = []
        for pattern, entity, score in zip(self.compiled_regexps, self.entities, self.score):
            ents += [NamedEntity(m.start(), m.end(), entity, m.group(), score, "re") for m in pattern.finditer(text)]
        return ents
