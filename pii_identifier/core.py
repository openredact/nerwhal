from dataclasses import dataclass
from typing import List

import pii_identifier.backends
from pii_identifier.recognizers import __all__ as all_recognizers


@dataclass
class PII:
    start: int
    end: int
    type: str
    text: str
    score: float  # get score: https://github.com/explosion/spaCy/issues/881
    model: str


@dataclass
class Score:
    f2: float


# STATE
# - with importing core, all the heavy work like loading models is done
# - calling find_piis creates a new transient pipe config


def find_piis(text: str, recognizers=all_recognizers, aggregation_strategy="keep_all") -> List[PII]:
    backends = {}
    for recognizer in recognizers:
        if recognizer.backend_type not in backends:
            # import backend modules only if they are used
            backend_cls = pii_identifier.backends.load(recognizer.backend_type)
            backends[recognizer.backend_type] = backend_cls()

        backends[recognizer.backend_type].register_recognizer(recognizer)

    results = []
    for backend in backends.values():
        results += backend.run(text)

    piis = _aggregate(*results, strategy=aggregation_strategy)

    return piis


def _aggregate(piis, *other_piis, strategy="keep_all"):
    # other strategies may include:
    # - merge: if piis of different type overlap keep the one with higher score, if they are of same type combine
    # - rigid: raise an error if piis overlap
    # maybe flags are handy too:
    # - rescore: if a pii is found twice, combine the scores

    if strategy == "keep_all":
        [piis.extend(other) for other in other_piis]
    else:
        raise ValueError(f"Unknown aggregation strategy {strategy}")
    return piis


def evaluate(piis: List[PII], gold: List[PII]) -> Score:
    pass


def tune(text: str, gold: List[PII]):
    pass
