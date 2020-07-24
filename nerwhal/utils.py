def _tokenize(text):

    return []


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
