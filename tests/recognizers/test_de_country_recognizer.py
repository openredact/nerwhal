import pytest

from pii_identifier.recognizers.de_country_recognizer import DeCountryRecognizer


@pytest.fixture
def backend(set_up_backend):
    recognizer = DeCountryRecognizer()
    backend = set_up_backend(recognizer)
    return backend


def test_single_word_country(backend, embed):
    text = "Finnland hat ein neues Gesetz erlassen."
    piis = backend.run(text)
    assert embed(text, piis) == "GPE hat ein neues Gesetz erlassen."


def test_multi_word_country(backend, embed):
    text = "Was ist die Hauptstadt der Republik Nordmazedonien?"
    piis = backend.run(text)
    assert embed(text, piis) == "Was ist die Hauptstadt der GPE?"


def test_declined_multi_word_country(backend, embed):
    text = "Was ist die Hauptstadt der Vereinigten Mexikanischen Staaten?"
    piis = backend.run(text)
    assert embed(text, piis) == "Was ist die Hauptstadt der GPE?"
