from nerwhal.backends.flashtext_backend import FlashtextBackend
from nerwhal.recognizer_bases import FlashtextRecognizer


def test_single_recognizer(embed):
    class TestRecognizer(FlashtextRecognizer):
        TAG = "XX"
        SCORE = 1.0

        @property
        def keywords(self):
            return ["abc", "cde"]

    backend = FlashtextBackend()
    backend.register_recognizer(TestRecognizer)
    text = "Das ist abc und cde."
    ents = backend.run(text)
    assert embed(text, ents) == "Das ist XX und XX."
    assert ents[0].start_char == 8
    assert ents[0].end_char == 11
    assert ents[0].tag == "XX"
    assert ents[0].text == "abc"
    assert ents[0].score == 1.0
    assert ents[0].recognizer == "TestRecognizer"


def test_multiple_recognizers(embed):
    class TestRecognizerA(FlashtextRecognizer):
        TAG = "A"
        SCORE = 1.0

        @property
        def keywords(self):
            return ["abc"]

    class TestRecognizerB(FlashtextRecognizer):
        TAG = "B"
        SCORE = 0.5

        @property
        def keywords(self):
            return ["cde"]

    backend = FlashtextBackend()
    backend.register_recognizer(TestRecognizerA)
    backend.register_recognizer(TestRecognizerB)
    text = "Das ist abc und cde."
    ents = backend.run(text)
    assert embed(text, ents) == "Das ist A und B."
    assert ents[0].tag == "A"
    assert ents[0].score == 1.0
    assert ents[1].tag == "B"
    assert ents[1].score == 0.5


def test_overlapping_recognizers(embed):
    class TestRecognizerA(FlashtextRecognizer):
        TAG = "A"
        SCORE = 1.0

        @property
        def keywords(self):
            return ["abc", "cde"]

    class TestRecognizerB(FlashtextRecognizer):
        TAG = "B"
        SCORE = 0.5

        @property
        def keywords(self):
            return ["cde", "fgh"]

    backend = FlashtextBackend()
    backend.register_recognizer(TestRecognizerA)
    backend.register_recognizer(TestRecognizerB)
    text = "Das ist cde."
    ents = backend.run(text)
    #  Recognizer B overwrites the keyword "cde"
    assert embed(text, ents) == "Das ist B."
