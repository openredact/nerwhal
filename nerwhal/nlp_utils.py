import subprocess


def load_stanza_nlp(language, processors):
    import stanza

    try:
        stanza_nlp = stanza.Pipeline(lang=language, processors=processors)
    except FileNotFoundError:
        stanza.download(language, processors=processors)
        stanza_nlp = stanza.Pipeline(lang=language, processors=processors)

    return stanza_nlp


def load_spacy_nlp(language, disable_components):
    import spacy

    try:
        spacy_nlp = spacy.load(language, disable=disable_components)
    except IOError:
        subprocess.run(["python", "-m", "spacy", "download", language])
        spacy_nlp = spacy.load(language, disable=disable_components)

    return spacy_nlp


def configure_entity_extension_attributes():
    from spacy.tokens import Span

    if not Span.has_extension("score"):
        Span.set_extension("score", default=-1.0)
    if not Span.has_extension("recognizer"):
        Span.set_extension("recognizer", default="")


def set_entity_extension_attributes(score, recognizer):
    def function(doc):
        for ent in doc.ents:
            if ent._.score >= 0:
                continue
            ent._.score = score
            ent._.recognizer = recognizer
        return doc

    return function
