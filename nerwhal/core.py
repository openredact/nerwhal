"""
This module implements the public API of the nerwhal.

The machine learning models are loaded once they are used first. That will be when a recognizer based on the respective
backend is used in `find_piis`.
"""
import importlib.util
import os
from collections import OrderedDict
from dataclasses import dataclass
from multiprocessing import Pipe
from multiprocessing.context import Process
from typing import List

import nerwhal.backends
from nerwhal.aggregation_strategies import aggregate
from nerwhal.backends.spacy_backend import SpacyBackend
from nerwhal.scorer import score_piis
from nerwhal.utils import _add_token_indices


@dataclass
class Pii:  # rename to NamedEntity
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
    load_examples: bool = False


class Core:
    def __init__(self):
        self.config = None
        self.backends = OrderedDict()

    def load_config_if_changed(self, config):
        if config == self.config:
            return

        self.config = config

        pipeline = SpacyBackend(self.config.model_name)
        self.backends = {"spacy": pipeline}

        if self.config.load_examples:
            for file in os.listdir("nerwhal/example_recognizers"):
                if file.endswith("_recognizer.py"):
                    example = os.path.join("nerwhal/example_recognizers", file)
                    if example not in self.config.recognizer_paths:
                        self.config.recognizer_paths.append(example)

        for recognizer_path in self.config.recognizer_paths:
            if not os.path.isfile(recognizer_path):
                raise ValueError(f"Configured recognizer {recognizer_path} is not a file")

            module_name = os.path.splitext(os.path.basename(recognizer_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, recognizer_path)
            module = importlib.util.module_from_spec(spec)
            class_name = "".join(word.title() for word in module_name.split("_"))
            spec.loader.exec_module(module)

            recognizer_cls = getattr(module, class_name)
            recognizer = recognizer_cls()
            if recognizer.backend not in self.backends.keys():
                # import backend modules only if they are used
                backend_cls = nerwhal.backends.load(recognizer.backend)
                self.backends[recognizer.backend] = backend_cls()

            self.backends[recognizer.backend].register_recognizer(recognizer)

    def run_recognition(self, text):
        def target(func, arg, pipe_end):
            pipe_end.send(func(arg))

        jobs = []
        pipe_conns = []
        for r in self.backends.values():
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
