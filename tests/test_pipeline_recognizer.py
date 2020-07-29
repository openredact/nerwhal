import pytest

from nerwhal.pipeline import Pipeline


@pytest.fixture(scope="module")
def pipeline():
    return Pipeline("de")


def test_simple_person(pipeline, embed):
    text = "Yoda war mein Lehrmeister."
    ents, _ = pipeline.run(text)
    assert embed(text, ents) == "PER war mein Lehrmeister."


def test_simple_location(pipeline, embed):
    text = "Die Jedis kennen das schöne Deutschland nicht."
    ents, _ = pipeline.run(text)
    assert embed(text, ents) == "Die PER kennen das schöne LOC nicht."


def test_simple_tokenization(pipeline):
    text = "Ein kurzer Satz."
    _, tokens = pipeline.run(text)
    assert tokens[0] == {"text": "Ein", "has_ws": True, "start_char": 0, "end_char": 3}
    assert tokens[1] == {"text": "kurzer", "has_ws": True, "start_char": 4, "end_char": 10}
    assert tokens[2] == {"text": "Satz", "has_ws": False, "start_char": 11, "end_char": 15}
    assert tokens[3] == {"text": ".", "has_ws": False, "start_char": 15, "end_char": 16}
