from typing import List

from nerwhal.nlp_utils import load_spacy_nlp, configure_spacy_entity_extension_attributes
from nerwhal.types import Token

configure_spacy_entity_extension_attributes()


class Tokenizer:
    def __init__(self, language):
        self.nlp = load_spacy_nlp(language, disable_components=["tagger", "ner"])
        self.doc = None

    def tokenize(self, text):
        self.doc = self.nlp(text)

    def get_tokens(self):
        return self._to_nerwhal_tokens(self.doc)

    def get_sentence_for_token(self, idx, exclude_tokens: List[int] = None):
        spacy_tokens = self.doc[idx].sent

        if exclude_tokens:
            spacy_tokens = [token for token in spacy_tokens if token.i not in exclude_tokens]

        return self._to_nerwhal_tokens(spacy_tokens)

    def _to_nerwhal_tokens(self, spacy_tokens):
        return [
            Token(
                text=token.text,
                has_ws=token.whitespace_ == " ",
                br_count=token.text.count("\n"),
                start_char=token.idx,
                end_char=token.idx + len(token),
            )
            for token in spacy_tokens
        ]
