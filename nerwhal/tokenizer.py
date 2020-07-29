from nerwhal.nlp_utils import load_spacy_nlp, configure_entity_extension_attributes


configure_entity_extension_attributes()


class Tokenizer:
    def __init__(self, language):
        self.nlp = load_spacy_nlp(language, disable_components=["tagger", "parser", "ner"])

    def run(self, text):
        doc = self.nlp(text)

        tokens = [
            {
                "text": token.text,
                "has_ws": token.whitespace_ == " ",
                "start_char": token.idx,
                "end_char": token.idx + len(token),
            }
            for token in doc
        ]
        return tokens
