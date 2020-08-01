import pytest


@pytest.fixture(scope="session")
def setup_backend():
    def function(backend: str, **kwargs):
        """Create a backend for the given recognizer and register the recognizer at it."""
        if backend == "re":
            from nerwhal.backends.re_backend import ReBackend

            backend = ReBackend()
        elif backend == "flashtext":
            from nerwhal.backends.flashtext_backend import FlashtextBackend

            backend = FlashtextBackend()
        elif backend == "entity-ruler":
            from nerwhal.backends.entity_ruler_backend import EntityRulerBackend

            backend = EntityRulerBackend(**kwargs)
        else:
            raise ValueError(f"Unknown backend {backend}")
        return backend

    return function
