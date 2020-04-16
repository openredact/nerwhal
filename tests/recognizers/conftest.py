import pytest


@pytest.fixture
def set_up_backend():
    def function(recognizer):
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
