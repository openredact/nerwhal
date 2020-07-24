"""
This module implements the public API of the nerwhal.

The machine learning models are loaded once they are used first. That will be when a recognizer based on the respective
backend is used in `find_piis`.
"""

from dataclasses import dataclass
from importlib import import_module
from multiprocessing import Pipe
from multiprocessing.context import Process
from typing import List

import nerwhal.backends
from nerwhal.aggregation_strategies import aggregate
from nerwhal.scorer import score_piis
from nerwhal.spacy_pipeline import SpacyPipeline
from nerwhal.utils import _add_token_indices


@dataclass
class Pii:
    start_char: int
    end_char: int
    tag: str
    text: str = None
    score: float = None  # TODO what as metric
    model: str = None
    start_tok: int = None
    end_tok: int = None


@dataclass
class Config:
    model_name: str
    recognizer_paths: List[str]


class Core:
    def __init__(self):
        self.config = None
        self.pipeline = None
        self.backends = {}

    def load_config_if_changed(self, config):
        if config == self.config:
            return

        self.config = config

        self.pipeline = SpacyPipeline(config.model_name)

        backends = {}
        for recognizer_path in config.recognizer_paths:
            recognizer_module = import_module("nerwhal.recognizers")
            recognizer_cls = getattr(recognizer_module, recognizer_path)
            recognizer = recognizer_cls()
            if recognizer.backend not in backends.keys():
                # import backend modules only if they are used
                if recognizer.backend in ["re", "flashtext"]:
                    backend_cls = nerwhal.backends.load(recognizer.backend)
                    backends[recognizer.backend] = backend_cls()

            if recognizer.backend in ["re", "flashtext"]:
                backends[recognizer.backend].register_recognizer(recognizer)
            elif recognizer.backend == "entity-ruler":
                self.pipeline.register_recognizer(recognizer)

    def run_recognition(self, text):
        runnables = [self.pipeline] + list(self.backends.values())

        def target(func, arg, pipe_end):
            pipe_end.send(func(arg))

        jobs = []
        pipe_conns = []
        for r in runnables:
            recv_end, send_end = Pipe(False)
            proc = Process(target=target, args=(r.run, text, send_end))
            jobs.append(proc)
            pipe_conns.append(recv_end)
            proc.start()

        for proc in jobs:
            proc.join()

        results = [conn.recv() for conn in pipe_conns]

        ents, tokens = results[0]  # pipeline additionally returns tokens
        list_of_ent_lists = [ents]
        for res in results[1:]:
            list_of_ent_lists += [res]

        return list_of_ent_lists, tokens


core = Core()


def recognize(text: str, config: Config, aggregation_strategy="keep_all") -> dict:
    """Find personally identifiable data in the given text and return it.

    :param text:
    :param recognizers: a list of classes that implement the `Recognizer` interface
    :param aggregation_strategy: choose from `keep_all`, `ensure_disjointness` and `merge`
    """
    core.load_config_if_changed(config)
    results, tokens = core.run_recognition(text)

    if len(results) == 0:
        piis = []
    else:
        piis = aggregate(*results, strategy=aggregation_strategy)

    _add_token_indices(piis, tokens)
    return {"piis": piis, "tokens": tokens}


def evaluate(piis: List[Pii], gold: List[Pii]) -> dict:  # TODO rename piis
    """Compute the scores of a list of found PIIs compared to the corresponding true PIIs.

    Each Pii is required to have the fields `start_char`, `end_char` and `tag` populated. The remaining fields
    are ignored.
    """
    return score_piis(piis, gold)
