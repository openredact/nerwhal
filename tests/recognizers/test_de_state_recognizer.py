import pytest

from pii_identifier.recognizers.de_state_recognizer import DeStateRecognizer


@pytest.fixture
def backend(set_up_backend):
    recognizer = DeStateRecognizer()
    backend = set_up_backend(recognizer)
    return backend


def test_single_word_state(backend, embed):
    text = "Finnland hat ein neues Gesetz erlassen."
    piis = backend.run(text)
    assert embed(text, piis) == "STATE hat ein neues Gesetz erlassen."


def test_multi_word_state(backend, embed):
    text = "Was ist die Hauptstadt der Republik Nordmazedonien?"
    piis = backend.run(text)
    assert embed(text, piis) == "Was ist die Hauptstadt der STATE?"


def test_declined_multi_word_state(backend, embed):
    text = "Was ist die Hauptstadt der Vereinigten Mexikanischen Staaten?"
    piis = backend.run(text)
    assert embed(text, piis) == "Was ist die Hauptstadt der STATE?"
