from importlib import import_module


def load(backend):
    """Dynamically load the requested backend module."""

    if backend == "re":
        mod = ".re_backend"
        cls = "ReBackend"
    elif backend == "flashtext":
        mod = ".flashtext_backend"
        cls = "FlashtextBackend"
    elif backend == "entity-ruler":
        mod = ".entity_ruler_backend"
        cls = "EntityRulerBackend"
    else:
        raise ValueError(f"Unknown backend type {backend}")

    backend_cls = getattr(import_module(mod, package="nerwhal.backends"), cls)
    return backend_cls
