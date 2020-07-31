import pytest

from nerwhal.integrated_recognizers.money_recognizer import MoneyRecognizer


@pytest.fixture(scope="module")
def de_backend(setup_backend):
    recognizer = MoneyRecognizer
    backend = setup_backend(recognizer.BACKEND, language="de")
    backend.register_recognizer(recognizer)
    return backend


@pytest.fixture(scope="module")
def en_backend(setup_backend):
    recognizer = MoneyRecognizer
    backend = setup_backend(recognizer.BACKEND, language="en")
    backend.register_recognizer(recognizer)
    return backend


def test_de_euro(de_backend, embed):
    text = "Das Brot kostet 1,50 €."
    ents = de_backend.run(text)
    assert embed(text, ents) == "Das Brot kostet MONEY."


def test_de_euro_w_dots(de_backend, embed):
    text = "Er möchte 1.000.000 € im Lotto gewinnen."
    ents = de_backend.run(text)
    assert embed(text, ents) == "Er möchte MONEY im Lotto gewinnen."


def test_de_dollar(de_backend, embed):
    text = "Das Brot kostet 1,50 $."
    ents = de_backend.run(text)
    assert embed(text, ents) == "Das Brot kostet MONEY."


def test_us_dollar(en_backend, embed):
    text = "The bread costs $1.50."
    ents = en_backend.run(text)
    assert embed(text, ents) == "The bread costs MONEY."


def test_us_euro_w_dots_and_space(en_backend, embed):
    text = "He'd like to win € 1,000,000 in the lottery."
    ents = en_backend.run(text)
    assert embed(text, ents) == "He'd like to win MONEY in the lottery."


def test_us_euro(en_backend, embed):
    text = "The bread costs €1.50."
    ents = en_backend.run(text)
    assert embed(text, ents) == "The bread costs MONEY."
