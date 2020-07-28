import stanza
from spacy.tokens import Span
from spacy_stanza import StanzaLanguage


def load_nlp(model_name, processors):
    try:
        snlp = stanza.Pipeline(lang=model_name, processors=processors)
    except FileNotFoundError:
        stanza.download(model_name, processors=processors)
        snlp = stanza.Pipeline(lang=model_name, processors=processors)

    nlp = StanzaLanguage(snlp)
    return nlp


def configure_entity_extension_attributes():
    if not Span.has_extension("score"):
        Span.set_extension("score", default=-1.0)
    if not Span.has_extension("model"):
        Span.set_extension("model", default="")


def set_entity_extension_attributes(score, model):
    def function(doc):
        for ent in doc.ents:
            if ent._.score >= 0:
                continue
            ent._.score = score
            ent._.model = model
        return doc

    return function
