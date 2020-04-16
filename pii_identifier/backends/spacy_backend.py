import spacy
from spacy.pipeline import EntityRuler
from spacy.tokens import Span

from pii_identifier import PII
from pii_identifier.backends.backend_base import NlpBackend
from pii_identifier.recognizers import SpacyStatisticalRecognizer
from pii_identifier.recognizers._spacy_recognizer_base import SpacyEntityRulerRecognizer

MODEL = "de_core_news_sm"

# do the heavy lifting at time of module import
nlp = spacy.load(MODEL, disable=["tagger", "parser"])

# configure spacy objects and language pipeline
if not Span.has_extension("precision"):
    Span.set_extension("precision", default=-1.0)
if not Span.has_extension("model"):
    Span.set_extension("model", default="")


def label_ents(score, model):
    def function(doc):
        for ent in doc.ents:
            if ent._.precision >= 0:
                continue
            ent._.precision = score
            ent._.model = model
        return doc

    return function


empty_ruler = EntityRuler(nlp)
nlp.add_pipe(empty_ruler, name="entityruler", before="ner")
nlp.add_pipe(label_ents(1.0, "spacy_entityruler"), name="label_entityruler_ents", after="entityruler")
nlp.add_pipe(label_ents(nlp.meta["accuracy"]["ents_p"], "spacy_de_core_news_sm"), name="label_ner_ents", after="ner")


class SpacyBackend(NlpBackend):
    with_statistical_ner = False
    entityruler_patterns = []

    def register_recognizer(self, recognizer):
        if isinstance(recognizer, SpacyStatisticalRecognizer):
            self.with_statistical_ner = True
        elif isinstance(recognizer, SpacyEntityRulerRecognizer):
            self.entityruler_patterns += recognizer.patterns
        else:
            raise TypeError(f"Trying to register recognizer with unsupported type {type(recognizer)}")

    def run(self, text):
        ruler = EntityRuler(nlp)
        ruler.add_patterns(self.entityruler_patterns)
        nlp.replace_pipe("entityruler", ruler)

        if self.with_statistical_ner:
            doc = nlp(text)
        else:
            with nlp.disable_pipes("ner"):
                doc = nlp(text)

        piis = []
        for ent in doc.ents:
            piis += [PII(ent.start_char, ent.end_char, ent.label_, ent.text, ent._.precision, ent._.model)]
        return piis
