class EntityAligner:
    """This class aligns the start and end characters of entities with a given tokenization.

    In general, entity recognition methods do not know about token borders and thus do not always align with the tokenization.
    The purpose of this class is to align the entities with the nearest larger token border, and to set the entities start and
    end token indices.
    """

    def __init__(self):
        self._char_to_token_idx = {}

    def align_entities_with_tokens(self, ents, tokens):
        """Alter the given entity objects to match the nearest larger token start and end char, and set their start and end
        token indices.

        :param ents: a list of NamedEntity objects
        :param tokens: a list of token objects
        """
        self._compute_char_to_token_idx_lookup(tokens)
        self._set_tokens_in_entities(ents)

    def _set_tokens_in_entities(self, ents):
        """Set the start and end token indices in the given entities.

        Note, that this may also alter the entities start and end characters.
        """
        for ent in ents:
            self._set_start_tok(ent)
            self._set_end_tok(ent)

    def _set_start_tok(self, ent):
        """Recursive function to align the start of the entity with the nearest token border."""
        try:
            ent.start_tok = self._char_to_token_idx[ent.start_char]
        except KeyError:
            # search for the nearest larger token border
            ent.start_char -= 1
            self._set_start_tok(ent)

    def _set_end_tok(self, ent):
        """Recursive function to align the end of the entity with the nearest token border."""
        try:
            # take the last character in the entity to get the token index and to create a slice take the next token
            ent.end_tok = self._char_to_token_idx[ent.end_char - 1] + 1
        except KeyError:
            # search for the nearest larger token border
            ent.end_char += 1
            self._set_end_tok(ent)

    def _compute_char_to_token_idx_lookup(self, tokens):
        """Computes a lookup table, that maps the first and last character of each token to its index in the document."""
        self._char_to_token_idx = {}

        char = 0
        for idx, token in enumerate(tokens):
            token_len = len(token.text)
            self._char_to_token_idx[char] = idx  # first character in token
            self._char_to_token_idx[char + token_len - 1] = idx  # last character in token

            char += token_len
            if token.has_ws:
                char += 1
