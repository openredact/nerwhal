from dataclasses import dataclass

import stanza
from spacy.pipeline import EntityRuler
from spacy.tokens import Span
from spacy_stanza import StanzaLanguage

# from nerwhal.core import Pii
from nerwhal.backends.base import NlpBackend

# configure spacy objects and language pipeline
if not Span.has_extension("precision"):
    Span.set_extension("precision", default=-1.0)
if not Span.has_extension("model"):
    Span.set_extension("model", default="")


@dataclass
class Pii:
    start_char: int
    end_char: int
    tag: str
    text: str = None
    score: float = None  # TODO what as metric
    model: str = None
    start_tok: int = None
    end_tok: int = None


# def label_ents(score, model):
#     def function(doc):
#         for ent in doc.ents:
#             if ent._.precision >= 0:
#                 continue
#             ent._.precision = score
#             ent._.model = model
#         return doc
#
#     return function


# nlp.add_pipe(label_ents(0.95, "spacy_entityruler"), name="label_entityruler_ents", after="entityruler")
#
# # get score: https://github.com/explosion/spaCy/issues/881
# nlp.add_pipe(label_ents(nlp.meta["accuracy"]["ents_p"] / 100, "spacy_" + MODEL), name="label_ner_ents", after="ner")


class SpacyPipeline(NlpBackend):
    def __init__(self, stanza_model):
        stanza.download(stanza_model, processors="tokenize,mwt,ner")

        snlp = stanza.Pipeline(lang=stanza_model, processors="tokenize,mwt,ner")
        self.nlp = StanzaLanguage(snlp)

        self.ruler = EntityRuler(self.nlp)
        self.nlp.add_pipe(self.ruler, "entityruler")

    def run(self, text):
        doc = self.nlp(text)

        piis = []
        for ent in doc.ents:
            piis += [Pii(ent.start_char, ent.end_char, ent.label_, ent.text, ent._.precision, ent._.model)]
        return (
            piis,
            [
                {
                    "text": token.text,
                    "has_ws": token.whitespace_ == " ",
                    "start_char": token.idx,
                    "end_char": token.idx + len(token),
                }
                for token in doc
            ],
        )

    def register_recognizer(self, recognizer):
        self.ruler.add_patterns(recognizer.rules)
