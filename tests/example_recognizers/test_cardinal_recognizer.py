import pytest

from nerwhal.example_recognizers.cardinal_recognizer import CardinalRecognizer


@pytest.fixture
def backend(setup_backend):
    recognizer = CardinalRecognizer
    backend = setup_backend(recognizer.BACKEND)
    backend.register_recognizer(recognizer)
    return backend


def test_cardinal(backend, embed):
    text = "Chewbacca wiegt 102 kg."
    ents = backend.run(text)
    assert embed(text, ents) == "Chewbacca wiegt CARDINAL kg."


def test_cardinal_wo_space(backend, embed):
    text = "Er fliegt mit 10000km/h."
    ents = backend.run(text)
    assert embed(text, ents) == "Er fliegt mit CARDINALkm/h."


def test_cardinal_w_dot(backend, embed):
    text = "Er fliegt mit 1.000.000 km/h."
    ents = backend.run(text)
    assert embed(text, ents) == "Er fliegt mit CARDINAL km/h."


def test_cardinal_w_comma(backend, embed):
    text = "Das maximale Gewicht für Handgepäck ist 9,99 kg."
    ents = backend.run(text)
    assert embed(text, ents) == "Das maximale Gewicht für Handgepäck ist CARDINAL kg."
