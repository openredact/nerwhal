from .base import Backend
from nerwhal.types import NamedEntity
from nerwhal.nlp_utils import load_stanza_nlp

# the stanza NER models have an F1 score between 74.3 and 94.8, https://stanfordnlp.github.io/stanza/performance.html
# we choose a hardcoded score in this scale
NER_SCORE = 0.8


class StanzaNerBackend(Backend):
    def __init__(self, language):
        self.stanza_nlp = load_stanza_nlp(language, processors="tokenize,mwt,ner")

    def register_recognizer(self, recognizer_cls):
        raise NotImplementedError()

    def run(self, text):
        doc = self.stanza_nlp(text)
        return [
            NamedEntity(ent.start_char, ent.end_char, ent.type, ent.text, NER_SCORE, self.__class__.__name__)
            for ent in doc.entities
        ]
