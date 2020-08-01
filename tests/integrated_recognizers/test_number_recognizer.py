import pytest

from nerwhal.integrated_recognizers.number_recognizer import NumberRecognizer


@pytest.fixture
def backend(setup_backend):
    recognizer = NumberRecognizer
    backend = setup_backend(recognizer.BACKEND)
    backend.register_recognizer(recognizer)
    return backend


def test_number(backend, embed):
    text = "Chewbacca wiegt 102 kg."
    ents = backend.run(text)
    assert embed(text, ents) == "Chewbacca wiegt NUMBER kg."


def test_number_wo_space(backend, embed):
    text = "Er fliegt mit 10000km/h."
    ents = backend.run(text)
    assert embed(text, ents) == "Er fliegt mit NUMBERkm/h."


def test_number_w_dot(backend, embed):
    text = "Er fliegt mit 1.000.000 km/h."
    ents = backend.run(text)
    assert embed(text, ents) == "Er fliegt mit NUMBER km/h."


def test_number_w_comma(backend, embed):
    text = "Das maximale Gewicht für Handgepäck ist 9,99 kg."
    ents = backend.run(text)
    assert embed(text, ents) == "Das maximale Gewicht für Handgepäck ist NUMBER kg."
