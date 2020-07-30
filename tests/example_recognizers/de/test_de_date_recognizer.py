import pytest

from nerwhal.example_recognizers.de.de_date_recognizer import DeDateRecognizer


@pytest.fixture(scope="module")
def backend(setup_backend):
    recognizer = DeDateRecognizer
    backend = setup_backend(recognizer.BACKEND, language="de")
    backend.register_recognizer(recognizer)
    return backend


# DIN 1355-1


def test_current_1355_1(backend, embed):
    text = "Der 25.06.1999 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_future_1355_1(backend, embed):
    text = "Der 25.12.2978 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_historic_1355_1(backend, embed):
    text = "Der 25.12.768 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_abbreviated_1355_1(backend, embed):
    text = "Der 5.12.74 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_1355_1_invalid_month(backend, embed):
    text = "Der 24.13.1999 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert len(ents) == 0


def test_1355_1_invalid_day(backend, embed):
    text = "Der 35.12.1999 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert len(ents) == 0


# DIN 5008


def test_current_5008(backend, embed):
    text = "Der 1999-06-25 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_future_5008(backend, embed):
    text = "Der 2978-12-25 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_5008_invalid_month(backend, embed):
    text = "Der 1999-13-25 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert len(ents) == 0


def test_5008_invalid_day(backend, embed):
    text = "Der 1999-12-35 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert len(ents) == 0


# Written out


def test_current_written_out(backend, embed):
    text = "Der 25. Juni 1999 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_future_written_out(backend, embed):
    text = "Der 25. Dezember 2978 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_historic_written_out(backend, embed):
    text = "Der 25. Dezember 768 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_abbreviated_written_out(backend, embed):
    text = "Der 5. Dez. 74 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "Der DATE ist ein zufälliges Datum."


def test_with_day_written_out(backend, embed):
    text = "Montag, 5. Dez. 74 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert embed(text, ents) == "DATE ist ein zufälliges Datum."


def test_written_out_invalid_month(backend, embed):
    text = "Der 24. Foobar 1999 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert len(ents) == 0


def test_written_out_invalid_day(backend, embed):
    text = "Der 35. Dezember 1999 ist ein zufälliges Datum."
    ents = backend.run(text)
    assert len(ents) == 0
