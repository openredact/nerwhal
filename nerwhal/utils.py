def add_token_indices(ents, tokens):
    pos_to_token_idx = {}

    pos = 0
    for idx, token in enumerate(tokens):
        token_len = len(token.text)
        pos_to_token_idx[pos] = idx  # start
        pos_to_token_idx[pos + token_len - 1] = idx  # end

        pos += token_len
        if token.has_ws:
            pos += 1

    for ent in ents:
        ent.start_tok = pos_to_token_idx[ent.start_char]
        ent.end_tok = pos_to_token_idx[ent.end_char - 1] + 1
