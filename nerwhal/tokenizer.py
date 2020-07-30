from nerwhal.nlp_utils import load_spacy_nlp, configure_entity_extension_attributes


configure_entity_extension_attributes()


class Tokenizer:
    def __init__(self, language):
        self.nlp = load_spacy_nlp(language, disable_components=["tagger", "ner"])
        self.doc = None

    def tokenize(self, text):
        self.doc = self.nlp(text)

    def get_tokens(self):
        tokens = [
            {
                "text": token.text,
                "has_ws": token.whitespace_ == " ",
                "start_char": token.idx,
                "end_char": token.idx + len(token),
            }
            for token in self.doc
        ]
        return tokens

    def get_sentence_for_token(self, i):
        return self.doc[i].sent
