import pytest

from nerwhal.backends.stanza_ner_backend import StanzaNerBackend


@pytest.fixture(scope="module")
def stanza_ner_backend():
    return StanzaNerBackend("de")


@pytest.mark.stanza
def test_simple_person(stanza_ner_backend, embed):
    text = "Yoda war mein Lehrmeister."
    ents = stanza_ner_backend.run(text)
    assert embed(text, ents) == "PER war mein Lehrmeister."


@pytest.mark.stanza
def test_simple_location(stanza_ner_backend, embed):
    text = "Wer kennt das schöne Deutschland nicht?"
    ents = stanza_ner_backend.run(text)
    assert embed(text, ents) == "Wer kennt das schöne LOC nicht?"


@pytest.mark.stanza
def test_multiple_ents(stanza_ner_backend, embed):
    text = "Meister Yoda macht in Berlin Urlaub."
    ents = stanza_ner_backend.run(text)
    assert embed(text, ents) == "Meister PER macht in LOC Urlaub."
