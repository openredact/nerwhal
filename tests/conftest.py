import pytest


@pytest.fixture(scope="session")
def embed():
    def function(text, ents):
        """Replace the text passages identified as personal data with their tag.

        E.g. "My name is Han." will embed a named entity for "Han" like this: "My name is PER."

        :param text:
        :param ents: a list of named entities, sorted in ascending order, without overlaps
        :return: the text with entities embedded into it
        """

        for ent in reversed(ents):
            text = text[: ent.start_char] + ent.tag + text[ent.end_char :]
        return text

    return function
