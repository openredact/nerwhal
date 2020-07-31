import pytest

from nerwhal.tokenizer import Tokenizer
from nerwhal.types import Token


@pytest.fixture(scope="module")
def tokenizer():
    return Tokenizer("de")


def test_simple_tokenization(tokenizer):
    text = "Ein kurzer Satz."
    tokenizer.tokenize(text)
    tokens = tokenizer.get_tokens()
    assert tokens[0] == Token(text="Ein", has_ws=True, has_br=False, start_char=0, end_char=3)
    assert tokens[1] == Token(text="kurzer", has_ws=True, has_br=False, start_char=4, end_char=10)
    assert tokens[2] == Token(text="Satz", has_ws=False, has_br=False, start_char=11, end_char=15)
    assert tokens[3] == Token(text=".", has_ws=False, has_br=False, start_char=15, end_char=16)


def test_that_contractions_are_not_expanded(tokenizer):
    text = "Wir geh'n zum Bus."
    tokenizer.tokenize(text)
    tokens = tokenizer.get_tokens()
    assert tokens[0] == Token(text="Wir", has_ws=True, has_br=False, start_char=0, end_char=3)
    assert tokens[1] == Token(text="geh'n", has_ws=True, has_br=False, start_char=4, end_char=9)
    assert tokens[2] == Token(text="zum", has_ws=True, has_br=False, start_char=10, end_char=13)
    assert tokens[3] == Token(text="Bus", has_ws=False, has_br=False, start_char=14, end_char=17)
    assert tokens[4] == Token(text=".", has_ws=False, has_br=False, start_char=17, end_char=18)


def test_single_line_break(tokenizer):
    text = "Han Solo und Wookiee Chewbacca wurden Freunde.\nHan's E-Mail ist han.solo@imperium.com."
    tokenizer.tokenize(text)
    tokens = tokenizer.get_tokens()
    assert 1 == len([t for t in tokens if t.has_br])


def test_double_line_breaks(tokenizer):
    text = "Han Solo und Wookiee Chewbacca wurden Freunde.\n\nHan's E-Mail ist han.solo@imperium.com."
    tokenizer.tokenize(text)
    tokens = tokenizer.get_tokens()
    assert 1 == len([t for t in tokens if t.has_br])


def test_line_breaks_in_several_positions(tokenizer):
    text = "Hi there!\nHan Solo und Wookiee Chewbacca wurden Freunde.\n\nHan's E-Mail ist han.solo@imperium.com."
    tokenizer.tokenize(text)
    tokens = tokenizer.get_tokens()
    assert 2 == len([t for t in tokens if t.has_br])
