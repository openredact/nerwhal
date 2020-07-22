import pytest

from nerwhal.recognizers import SpacyStatisticalRecognizer


@pytest.fixture(params=[SpacyStatisticalRecognizer()])
def stat_recognizer(request):
    return request.param


@pytest.fixture
def set_up_backend():
    def function(recognizer):
        """Create a backend for the given recognizer and register the recognizer at it."""
        if recognizer.backend == "spacy":
            from nerwhal.backends.spacy_backend import SpacyBackend

            backend = SpacyBackend()
        elif recognizer.backend == "re":
            from nerwhal.backends.re_backend import ReBackend

            backend = ReBackend()
        else:
            raise ValueError(f"Unknown backend {recognizer.backend}")

        backend.register_recognizer(recognizer)
        return backend

    return function
