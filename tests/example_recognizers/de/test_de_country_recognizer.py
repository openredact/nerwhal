import pytest

from nerwhal.example_recognizers.de.de_country_recognizer import DeCountryRecognizer


@pytest.fixture(scope="module")
def backend(setup_backend):
    recognizer = DeCountryRecognizer
    backend = setup_backend(recognizer.BACKEND)
    backend.register_recognizer(recognizer)
    return backend


def test_single_word_country(backend, embed):
    text = "Finnland hat ein neues Gesetz erlassen."
    ents = backend.run(text)
    assert embed(text, ents) == "COUNTRY hat ein neues Gesetz erlassen."


def test_multi_word_country(backend, embed):
    text = "Was ist die Hauptstadt der Republik Nordmazedonien?"
    ents = backend.run(text)
    assert embed(text, ents) == "Was ist die Hauptstadt der COUNTRY?"


def test_declined_multi_word_country(backend, embed):
    text = "Was ist die Hauptstadt der Demokratischen Volksrepublik Laos?"
    ents = backend.run(text)
    assert embed(text, ents) == "Was ist die Hauptstadt der COUNTRY?"
