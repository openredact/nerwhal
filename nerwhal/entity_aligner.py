class EntityAligner:
    def __init__(self):
        self._char_to_token_idx = {}

    def align_entities_with_tokens(self, ents, tokens):
        self._compute_char_to_token_idx_lookup(tokens)
        self._set_tokens_in_entities(ents)

    def _set_tokens_in_entities(self, ents):
        for ent in ents:
            self._set_start_tok(ent)
            self._set_end_tok(ent)

    def _set_start_tok(self, ent):
        try:
            ent.start_tok = self._char_to_token_idx[ent.start_char]
        except KeyError:
            # search for the nearest larger token border
            ent.start_char -= 1
            self._set_start_tok(ent)

    def _set_end_tok(self, ent):
        try:
            # take the last character in the entity to get the token index and to create a slice take the next token
            ent.end_tok = self._char_to_token_idx[ent.end_char - 1] + 1
        except KeyError:
            # search for the nearest larger token border
            ent.end_char += 1
            self._set_end_tok(ent)

    def _compute_char_to_token_idx_lookup(self, tokens):
        self._char_to_token_idx = {}

        char = 0
        for idx, token in enumerate(tokens):
            token_len = len(token.text)
            self._char_to_token_idx[char] = idx  # first character in token
            self._char_to_token_idx[char + token_len - 1] = idx  # last character in token

            char += token_len
            if token.has_ws:
                char += 1
