"""
This module implements the public API of the nerwhal.

The machine learning models are loaded once they are used first. That will be when a recognizer based on the respective
backend is used in `find_piis`.
"""

from dataclasses import dataclass
from importlib import import_module
from typing import List

import nerwhal.backends
from nerwhal.aggregation_strategies import aggregate
from nerwhal.recognizers import __all__ as all_recognizers
from nerwhal.scorer import score_piis
from nerwhal.utils import _tokenize, _add_token_indices


@dataclass
class Pii:
    start_char: int
    end_char: int
    tag: str
    text: str = None
    score: float = None  # the confidence that this text passage is a Pii of the stated tag
    model: str = None
    start_tok: int = None
    end_tok: int = None


def find_piis(text: str, recognizers=all_recognizers, aggregation_strategy="keep_all") -> dict:
    """Find personally identifiable data in the given text and return it.

    :param text:
    :param recognizers: a list of classes that implement the `Recognizer` interface
    :param aggregation_strategy: choose from `keep_all`, `ensure_disjointness` and `merge`
    """
    recognizer_module = import_module("nerwhal.recognizers")
    backends = {}
    for recognizer_name in recognizers:
        recognizer_cls = getattr(recognizer_module, recognizer_name)
        recognizer = recognizer_cls()
        if recognizer.backend not in backends:
            # import backend modules only if they are used
            backend_cls = nerwhal.backends.load(recognizer.backend)
            backends[recognizer.backend] = backend_cls()

        backends[recognizer.backend].register_recognizer(recognizer)

    results = ()
    for backend in backends.values():
        results += (backend.run(text),)

    if len(results) == 0:
        piis = []
    else:
        piis = aggregate(*results, strategy=aggregation_strategy)

    tokens = _tokenize(text)
    _add_token_indices(piis, tokens)
    return {"piis": piis, "tokens": tokens}


def evaluate(piis: List[Pii], gold: List[Pii]) -> dict:  # TODO rename piis
    """Compute the scores of a list of found PIIs compared to the corresponding true PIIs.

    Each Pii is required to have the fields `start_char`, `end_char` and `tag` populated. The remaining fields
    are ignored.
    """
    return score_piis(piis, gold)
