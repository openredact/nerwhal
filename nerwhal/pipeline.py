from nerwhal.nlp_utils import load_nlp, configure_entity_extension_attributes, set_entity_extension_attributes
from nerwhal.types import NamedEntity


# the stanza NER models have an F1 score between 74.3 and 94.8, https://stanfordnlp.github.io/stanza/performance.html
# we choose a hardcoded score in this scale
NER_SCORE = 0.8

configure_entity_extension_attributes()


class Pipeline:
    def __init__(self, stanza_model):
        self.nlp = load_nlp(stanza_model, "tokenize,ner")
        self.nlp.add_pipe(set_entity_extension_attributes(NER_SCORE, self.nlp.meta["lang"]), name="label_ner_ents")

    def run(self, text):
        doc = self.nlp(text)

        ents = []
        for ent in doc.ents:
            ents += [NamedEntity(ent.start_char, ent.end_char, ent.label_, ent.text, ent._.score, ent._.model)]

        tokens = [
            {
                "text": token.text,
                "has_ws": token.whitespace_ == " ",
                "start_char": token.idx,
                "end_char": token.idx + len(token),
            }
            for token in doc
        ]
        return ents, tokens
