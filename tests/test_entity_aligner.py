from nerwhal import NamedEntity
from nerwhal.tokenizer import Tokenizer
from nerwhal.types import Token
from nerwhal.entity_aligner import EntityAligner


def test_align_entities_with_tokens():
    text = "Han's Telefonnummer ist 0049 1234 5678567."
    tokenizer = Tokenizer("de")
    tokenizer.tokenize(text)
    tokens = tokenizer.get_tokens()

    assert tokens == [
        Token(text="Han's", has_ws=True, br_count=0, start_char=0, end_char=5),
        Token(text="Telefonnummer", has_ws=True, br_count=0, start_char=6, end_char=19),
        Token(text="ist", has_ws=True, br_count=0, start_char=20, end_char=23),
        Token(text="0049", has_ws=True, br_count=0, start_char=24, end_char=28),
        Token(text="1234", has_ws=True, br_count=0, start_char=29, end_char=33),
        Token(text="5678567.", has_ws=False, br_count=0, start_char=34, end_char=42),
    ]

    ents = [
        NamedEntity(start_char=0, end_char=5, tag="PER", text="Han's", score=1.0, recognizer="Test"),
        NamedEntity(start_char=24, end_char=41, tag="PHONE", text="0049 1234 5678567", score=1.0, recognizer="Test"),
        NamedEntity(start_char=13, end_char=19, tag="JUST_A_DUMMY", text="nummer", score=0.0, recognizer=""),
    ]

    entity_aligner = EntityAligner()
    entity_aligner.align_entities_with_tokens(ents, tokens)
    assert ents[0].start_tok == 0
    assert ents[0].end_tok == 1

    assert ents[1].start_tok == 3
    assert ents[1].end_tok == 6
    assert ents[1].start_char == 24
    assert ents[1].end_char == 42

    assert ents[2].start_tok == 1
    assert ents[2].end_tok == 2
    assert ents[2].start_char == 6
    assert ents[2].end_char == 19
