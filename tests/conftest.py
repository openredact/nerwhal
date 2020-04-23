import pytest


@pytest.fixture
def embed():
    def function(text, piis):
        """Replace the text passages identified as personal data with their type label.

        E.g. "My name is Han." will embed a PII for "Han" like this: "My name is PER."

        :param text:
        :param piis: a list of PIIs, sorted in ascending order, without overlaps
        :return: the text with PIIs embedded into it
        """

        for pii in reversed(piis):
            text = text[: pii.start] + pii.type + text[pii.end :]
        return text

    return function
