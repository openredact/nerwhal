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
    type: str
    text: str
    score: float
    model: str


# STATE
# - with importing core, all the heavy work like loading models is done
# - calling find_piis creates a new transient pipe config


def find_piis(text: str, recognizers=all_recognizers, aggregation_strategy="keep_all") -> List[Pii]:
    backends = {}
    for recognizer_cls in recognizers:
        recognizer = recognizer_cls()
        if recognizer.backend not in backends:
            # import backend modules only if they are used
            backend_cls = pii_identifier.backends.load(recognizer.backend)
            backends[recognizer.backend] = backend_cls()

        backends[recognizer.backend].register_recognizer(recognizer)

    results = []
    for backend in backends.values():
        results += [backend.run(text)]

    piis = aggregate(*results, strategy=aggregation_strategy)

    return piis


def evaluate(piis: List[Pii], gold: List[Pii]) -> dict:
    return score_piis(piis, gold)


def tune(text: str, gold: List[Pii]):
    raise NotImplementedError
