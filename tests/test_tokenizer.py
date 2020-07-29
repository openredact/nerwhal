import pytest

from nerwhal.tokenizer import Tokenizer


@pytest.fixture(scope="module")
def tokenizer():
    return Tokenizer("de")


def test_simple_tokenization(tokenizer):
    text = "Ein kurzer Satz."
    tokens = tokenizer.run(text)
    assert tokens[0] == {"text": "Ein", "has_ws": True, "start_char": 0, "end_char": 3}
    assert tokens[1] == {"text": "kurzer", "has_ws": True, "start_char": 4, "end_char": 10}
    assert tokens[2] == {"text": "Satz", "has_ws": False, "start_char": 11, "end_char": 15}
    assert tokens[3] == {"text": ".", "has_ws": False, "start_char": 15, "end_char": 16}


def test_that_contractions_are_not_expanded(tokenizer):
    text = "Wir geh'n zum Bus."
    tokens = tokenizer.run(text)
    assert tokens[0] == {"text": "Wir", "has_ws": True, "start_char": 0, "end_char": 3}
    assert tokens[1] == {"text": "geh'n", "has_ws": True, "start_char": 4, "end_char": 9}
    assert tokens[2] == {"text": "zum", "has_ws": True, "start_char": 10, "end_char": 13}
    assert tokens[3] == {"text": "Bus", "has_ws": False, "start_char": 14, "end_char": 17}
    assert tokens[4] == {"text": ".", "has_ws": False, "start_char": 17, "end_char": 18}
