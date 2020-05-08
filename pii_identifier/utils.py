def _tokenize(text):
    from pii_identifier.backends.spacy_backend import nlp

    doc = nlp(text)
    return [(token.text, token.whitespace_ == " ") for token in doc]


def _translate_to_token_based(piis, tokenization):
    pos_to_token_idx = {}

    pos = 0
    for idx, (token_text, token_has_ws) in enumerate(tokenization):
        token_len = len(token_text)
        pos_to_token_idx[pos] = idx  # start
        pos_to_token_idx[pos + token_len - 1] = idx  # end

        pos += token_len
        if token_has_ws:
            pos += 1

    for pii in piis:
        pii.start = pos_to_token_idx[pii.start]
        pii.end = pos_to_token_idx[pii.end - 1] + 1

    return piis
