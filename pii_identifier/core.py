"""
This module implements the public API of the pii_identifier.

The machine learning models are loaded once they are used first. That will be when a recognizer based on the respective
backend is used in `find_piis`.
"""

from dataclasses import dataclass
from typing import List

import pii_identifier.backends
from pii_identifier.aggregation_strategies import aggregate
from pii_identifier.recognizers import __all__ as all_recognizers
from pii_identifier.scorer import score_piis


@dataclass
class Pii:
    start: int
    end: int
    tag: str
    text: str
    score: float  # the confidence that this text passage is a Pii of the stated tag
    model: str


def find_piis(text: str, recognizers=all_recognizers, aggregation_strategy="keep_all") -> List[Pii]:
    """Find personally identifiable data in the given text and return it.

    :param text:
    :param recognizers: a list of classes that implement the `Recognizer` interface
    :param aggregation_strategy: choose from `keep_all`, `ensure_disjointness` and `merge`
    :param as_tokens: the default is to return the PIIs based on indices in the input text, if true
        return the PIIs based on the index of the text's tokens together with its tokenization
    """
    backends = {}
    for recognizer_cls in recognizers:
        recognizer = recognizer_cls()
        if recognizer.backend not in backends:
            # import backend modules only if they are used
            backend_cls = pii_identifier.backends.load(recognizer.backend)
            backends[recognizer.backend] = backend_cls()

        backends[recognizer.backend].register_recognizer(recognizer)

    results = ()
    for backend in backends.values():
        results += (backend.run(text),)

    piis = aggregate(*results, strategy=aggregation_strategy)

    return piis


def evaluate(piis: List[Pii], gold: List[Pii]) -> dict:
    """Compute the scores of a list of found PIIs compared to the corresponding true PIIs."""
    return score_piis(piis, gold)


def tune(text: str, gold: List[Pii]):
    """Improve the machine learning models with the provided examples."""
    raise NotImplementedError
