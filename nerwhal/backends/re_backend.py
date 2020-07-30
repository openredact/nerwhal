import re
from typing import Type

from .base import Backend
from nerwhal.types import NamedEntity
from ..recognizer_bases import ReRecognizer


class ReBackend(Backend):
    def __init__(self):
        self.compiled_regexps = []
        self.recognizer_classes = []

    def register_recognizer(self, recognizer_cls: Type[ReRecognizer]):
        recognizer = recognizer_cls()

        self.compiled_regexps += [re.compile(recognizer.regexp, flags=recognizer.FLAGS)]
        self.recognizer_classes.append(recognizer_cls)

    def run(self, text):
        ents = []
        for pattern, rec in zip(self.compiled_regexps, self.recognizer_classes):
            ents += [
                NamedEntity(*m.span(rec.GROUP), rec.TAG, m.group(rec.GROUP), rec.SCORE, rec.__name__)
                for m in pattern.finditer(text)
            ]
        return ents
