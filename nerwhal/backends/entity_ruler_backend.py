from typing import Type

from spacy.pipeline import EntityRuler

from .base import Backend
from nerwhal.recognizer_bases import EntityRulerRecognizer
from nerwhal.types import NamedEntity
from nerwhal.nlp_utils import configure_entity_extension_attributes, set_entity_extension_attributes, load_spacy_nlp

configure_entity_extension_attributes()


class EntityRulerBackend(Backend):
    def __init__(self, language):
        self.nlp = load_spacy_nlp(language, disable_components=["tagger", "parser", "ner"])

    def register_recognizer(self, recognizer_cls: Type[EntityRulerRecognizer]):
        recognizer = recognizer_cls()

        name = recognizer_cls.__name__
        ruler = EntityRuler(self.nlp)
        self.nlp.add_pipe(ruler, name)
        rules = [{"label": recognizer.TAG, "pattern": pattern} for pattern in recognizer.patterns]
        ruler.add_patterns(rules)
        self.nlp.add_pipe(set_entity_extension_attributes(recognizer.SCORE, name), name="label_" + name, after=name)

    def run(self, text):
        doc = self.nlp(text)

        ents = []
        for ent in doc.ents:
            ents += [NamedEntity(ent.start_char, ent.end_char, ent.label_, ent.text, ent._.score, ent._.model)]

        return ents
