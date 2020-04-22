import re

from pii_identifier import Pii
from pii_identifier.backends.backend_base import NlpBackend


class ReBackend(NlpBackend):
    def __init__(self):
        self.recognizers = []

    def register_recognizer(self, recognizer):
        self.recognizers += [recognizer]

    def run(self, text):
        piis = []
        for recognizer in self.recognizers:
            entity = recognizer.entity
            score = recognizer.precision
            pattern = re.compile(recognizer.regexp, flags=re.MULTILINE | re.VERBOSE)
            piis += [Pii(m.start(), m.end(), entity, m.group(), score, "re") for m in pattern.finditer(text)]
        return piis
