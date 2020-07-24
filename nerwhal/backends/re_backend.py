import re

from nerwhal import Pii
from nerwhal.backends.base import Backend


class ReBackend(Backend):
    def __init__(self):
        self.compiled_regexps = []
        self.entities = []
        self.precisions = []

    def register_recognizer(self, recognizer):
        self.compiled_regexps += [re.compile(recognizer.regexp, flags=recognizer.flags)]
        self.entities.append(recognizer.entity)
        self.precisions.append(recognizer.precision)

    def run(self, text):
        piis = []
        for pattern, entity, precision in zip(self.compiled_regexps, self.entities, self.precisions):
            piis += [Pii(m.start(), m.end(), entity, m.group(), precision, "re") for m in pattern.finditer(text)]
        return piis
