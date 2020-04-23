import pytest

from pii_identifier.recognizers import FlairStatisticalRecognizer
from pii_identifier.recognizers import SpacyStatisticalRecognizer


@pytest.fixture(params=[SpacyStatisticalRecognizer(), pytest.param(FlairStatisticalRecognizer(), marks=pytest.mark.slow)])
def stat_recognizer(request):
    return request.param


@pytest.fixture
def set_up_backend():
    def function(recognizer):
        """Create a backend for the given recognizer and register the recognizer at it."""
        if recognizer.backend == "spacy":
            from pii_identifier.backends.spacy_backend import SpacyBackend

            backend = SpacyBackend()
        elif recognizer.backend == "re":
            from pii_identifier.backends.re_backend import ReBackend

            backend = ReBackend()
        elif recognizer.backend == "flair":
            from pii_identifier.backends.flair_backend import FlairBackend

            backend = FlairBackend()
        else:
            raise ValueError(f"Unknown backend {recognizer.backend}")

        backend.register_recognizer(recognizer)
        return backend

    return function
