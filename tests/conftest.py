import pytest


@pytest.fixture
def embed():
    def function(text, piis):
        """Replace the text passages identified as piis with their type label.

        E.g. "My name is Han." will embed a Pii for "Han" like this: "My name is PER."

        Note, that `piis` has to be sorted in ascending order and that no piis may overlap.
        """

        for pii in reversed(piis):
            text = text[: pii.start] + pii.type + text[pii.end :]
        return text

    return function
