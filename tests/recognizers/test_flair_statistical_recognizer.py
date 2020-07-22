import pytest

from nerwhal.recognizers import FlairStatisticalRecognizer


@pytest.mark.slow
def test_multiple_sentences(set_up_backend, embed):
    backend = set_up_backend(FlairStatisticalRecognizer())
    text = (
        "Wookiee Chewbacca sollte Han Solo eigentlich fressen.\n"
        "Han und Wookiee sind aber zusammen geflohen. Wookie zog später nach Kashyyyk."
    )
    piis = backend.run(text)
    print(piis)
    assert (
        embed(text, piis) == "PER sollte PER eigentlich fressen.\n"
        "PER und PER sind aber zusammen geflohen. PER zog später nach LOC."
    )
