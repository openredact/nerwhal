from nerwhal.backends.entity_ruler_backend import EntityRulerBackend
from nerwhal.recognizer_bases import EntityRulerRecognizer


def test_single_recognizer(embed):
    class TestRecognizer(EntityRulerRecognizer):
        TAG = "TEST"
        SCORE = 1.0

        @property
        def patterns(self):
            return [[{"TEXT": "abc"}, {"TEXT": "cde"}]]

    backend = EntityRulerBackend("de")
    backend.register_recognizer(TestRecognizer)
    text = "Das ist abc cde."
    ents = backend.run(text)
    assert embed(text, ents) == "Das ist TEST."
    assert ents[0].start_char == 8
    assert ents[0].end_char == 15
    assert ents[0].tag == "TEST"
    assert ents[0].text == "abc cde"
    assert ents[0].score == 1.0
    assert ents[0].model == "entity-ruler_TestRecognizer"


def test_multiple_recognizers(embed):
    class TestRecognizerA(EntityRulerRecognizer):
        TAG = "A"
        SCORE = 1.0

        @property
        def patterns(self):
            return [[{"TEXT": "abc"}]]

    class TestRecognizerB(EntityRulerRecognizer):
        TAG = "B"
        SCORE = 0.5

        @property
        def patterns(self):
            return [[{"TEXT": "cde"}]]

    backend = EntityRulerBackend("de")
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
    class TestRecognizerA(EntityRulerRecognizer):
        TAG = "A"
        SCORE = 1.0

        @property
        def patterns(self):
            return [[{"TEXT": "abc"}, {"TEXT": "cde"}]]

    class TestRecognizerB(EntityRulerRecognizer):
        TAG = "B"
        SCORE = 0.5

        @property
        def patterns(self):
            return [[{"TEXT": "cde"}, {"TEXT": "efg"}]]

    class TestRecognizerC(EntityRulerRecognizer):
        TAG = "C"
        SCORE = 0.7

        @property
        def patterns(self):
            return [[{"TEXT": "cde"}, {"TEXT": "efg"}, {"TEXT": "ghi"}]]

    backend = EntityRulerBackend("de")
    backend.register_recognizer(TestRecognizerA)
    backend.register_recognizer(TestRecognizerB)
    backend.register_recognizer(TestRecognizerC)
    text = "Das sind abc cde efg und abc cde efg ghi."
    ents = backend.run(text)
    #  The first match wins
    assert embed(text, ents) == "Das sind A efg und A efg ghi."
