import pytest

from pii_identifier.recognizers import FlairStatisticalRecognizer


# TODO how to skip loading flair library with -m "not slow"
@pytest.mark.slow
def test_simple_persons(set_up_backend):
    recognizer = FlairStatisticalRecognizer()
    backend = set_up_backend(recognizer)
    piis = backend.run("Mein Lehrmeister war Yoda.")
    assert len(piis) == 1
    assert piis[0].type == "PER"
    assert piis[0].text == "Yoda"
