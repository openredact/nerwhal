import subprocess


def load_stanza_nlp(language, processors):
    """Load the Stanza nlp object.

    If the language's models cannot be found, they are downloaded.
    """
    import stanza

    try:
        stanza_nlp = stanza.Pipeline(lang=language, processors=processors)
    except (Exception, SystemExit):
        stanza.download(language, processors=processors)
        stanza_nlp = stanza.Pipeline(lang=language, processors=processors)

    return stanza_nlp


def load_spacy_nlp(language, disable_components):
    """Load the spaCy nlp object.

    If the language's models cannot be found, they are downloaded.
    """
    import spacy

    try:
        spacy_nlp = spacy.load(language, disable=disable_components)
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", language])
        spacy_nlp = spacy.load(language, disable=disable_components)

    return spacy_nlp


def configure_spacy_entity_extension_attributes():
    """Add custom extension attributes to the spaCy Span class."""
    from spacy.tokens import Span

    if not Span.has_extension("score"):
        Span.set_extension("score", default=-1.0)
    if not Span.has_extension("recognizer"):
        Span.set_extension("recognizer", default="")


def set_spacy_entity_extension_attributes(score, recognizer):
    """Returns a spaCy pipeline component, that sets the score and recognizer in a doc's entities."""

    def function(doc):
        for ent in doc.ents:
            if ent._.score >= 0:
                continue
            ent._.score = score
            ent._.recognizer = recognizer
        return doc

    return function
