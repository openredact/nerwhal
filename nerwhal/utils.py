def _tokenize(text):
    from nerwhal.backends.spacy_backend import nlp

    doc = nlp(text)

    return [
        {
            "text": token.text,
            "has_ws": token.whitespace_ == " ",
            "br_count": token.text.count("\n"),
            "start_char": token.idx,
            "end_char": token.idx + len(token),
        }
        for token in doc
    ]


def _add_token_indices(piis, tokenization):
    pos_to_token_idx = {}

    pos = 0
    for idx, token in enumerate(tokenization):
        token_len = len(token["text"])
        pos_to_token_idx[pos] = idx  # start
        pos_to_token_idx[pos + token_len - 1] = idx  # end

        pos += token_len
        if token["has_ws"]:
            pos += 1

    for pii in piis:
        pii.start_tok = pos_to_token_idx[pii.start_char]
        pii.end_tok = pos_to_token_idx[pii.end_char - 1] + 1
