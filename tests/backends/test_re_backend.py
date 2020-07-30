from nerwhal.backends.re_backend import ReBackend
from nerwhal.recognizer_bases import ReRecognizer


def test_single_recognizer(embed):
    class TestRecognizer(ReRecognizer):
        TAG = "TEST"
        SCORE = 1.0

        @property
        def regexp(self):
            return r"abc"

    backend = ReBackend()
    backend.register_recognizer(TestRecognizer)
    text = "Das ist abc und abc."
    ents = backend.run(text)
    assert embed(text, ents) == "Das ist TEST und TEST."
    assert ents[0].start_char == 8
    assert ents[0].end_char == 11
    assert ents[0].tag == "TEST"
    assert ents[0].text == "abc"
    assert ents[0].score == 1.0
    assert ents[0].model == "re"


def test_multiple_recognizers(embed):
    class TestRecognizerA(ReRecognizer):
        TAG = "A"
        SCORE = 1.0

        @property
        def regexp(self):
            return r"abc"

    class TestRecognizerB(ReRecognizer):
        TAG = "B"
        SCORE = 0.5

        @property
        def regexp(self):
            return r"123"

    backend = ReBackend()
    backend.register_recognizer(TestRecognizerA)
    backend.register_recognizer(TestRecognizerB)
    text = "Das ist abc und 123."
    ents = backend.run(text)
    assert embed(text, ents) == "Das ist A und B."
    assert ents[0].tag == "A"
    assert ents[0].score == 1.0
    assert ents[1].tag == "B"
    assert ents[1].score == 0.5


def test_overlapping_recognizers(embed):
    class TestRecognizerA(ReRecognizer):
        TAG = "A"
        SCORE = 1.0

        @property
        def regexp(self):
            return r"abc"

    class TestRecognizerB(ReRecognizer):
        TAG = "B"
        SCORE = 0.5

        @property
        def regexp(self):
            return r"ab"

    backend = ReBackend()
    backend.register_recognizer(TestRecognizerA)
    backend.register_recognizer(TestRecognizerB)
    text = "Das ist abc."
    ents = backend.run(text)
    assert ents[0].start_char == 8
    assert ents[0].end_char == 11
    assert ents[0].tag == "A"
    assert ents[0].text == "abc"

    assert ents[1].start_char == 8
    assert ents[1].end_char == 10
    assert ents[1].tag == "B"
    assert ents[1].text == "ab"
