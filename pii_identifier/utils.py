def _tokenize(text):
    from pii_identifier.backends.spacy_backend import nlp

    doc = nlp(text)
    return [(token.text, token.whitespace_ == " ") for token in doc]


def _add_token_indices(piis, tokenization):
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
        pii.start_tok = pos_to_token_idx[pii.start_char]
        pii.end_tok = pos_to_token_idx[pii.end_char - 1] + 1
