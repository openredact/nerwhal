import importlib.util
import os
from collections import OrderedDict
from multiprocessing import Pipe
from multiprocessing.context import Process
from typing import List

import nerwhal.backends
from nerwhal.aggregation_strategies import aggregate
from nerwhal.backends.stanza_ner_backend import StanzaNerBackend
from nerwhal.tokenizer import Tokenizer
from nerwhal.scorer import score_entities
from nerwhal.types import Config, NamedEntity
from nerwhal.utils import add_token_indices

EXAMPLE_RECOGNIZERS_PATH = "nerwhal/example_recognizers"


class Core:
    def __init__(self):
        self.config = None
        self.backends = OrderedDict()
        self.tokenizer = None

    def update_config(self, config):
        if config == self.config:
            return

        self.config = config

        self.tokenizer = Tokenizer(self.config.language)

        self.backends = {}

        if self.config.use_statistical_ner:
            self.backends["stanza"] = StanzaNerBackend(self.config.language)

        if self.config.load_example_recognizers:
            self._add_examples_to_config_recognizer_paths()

        for recognizer_path in self.config.recognizer_paths:
            if not os.path.isfile(recognizer_path):
                raise ValueError(f"Configured recognizer {recognizer_path} is not a file")

            recognizer_cls = self._load_class(recognizer_path)

            # import only the backend modules that are configured
            if recognizer_cls.BACKEND not in self.backends.keys():
                backend_cls = nerwhal.backends.load(recognizer_cls.BACKEND)

                if recognizer_cls.BACKEND == "entity_ruler":
                    backend_inst = backend_cls(self.config.language)
                else:
                    backend_inst = backend_cls()

                self.backends[recognizer_cls.BACKEND] = backend_inst

            self.backends[recognizer_cls.BACKEND].register_recognizer(recognizer_cls)

    def _load_class(self, recognizer_path):
        module_name = os.path.splitext(os.path.basename(recognizer_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, recognizer_path)
        module = importlib.util.module_from_spec(spec)
        class_name = "".join(word.title() for word in module_name.split("_"))
        spec.loader.exec_module(module)
        recognizer_cls = getattr(module, class_name)
        return recognizer_cls

    def _add_examples_to_config_recognizer_paths(self):
        for file in os.listdir(EXAMPLE_RECOGNIZERS_PATH):
            if file.endswith("_recognizer.py"):
                example = os.path.join(EXAMPLE_RECOGNIZERS_PATH, file)
                if example not in self.config.recognizer_paths:
                    self.config.recognizer_paths.append(example)

    def run_recognition(self, text):
        list_of_ent_lists = self._run_in_parallel(self.backends.values(), text)
        return list_of_ent_lists

    def run_tokenizer(self, text):
        tokens = self.tokenizer.run(text)
        return tokens

    def _run_in_parallel(self, backends, text):
        def target(func, arg, pipe_end):
            pipe_end.send(func(arg))

        jobs = []
        pipe_conns = []
        for backend in backends:
            recv_end, send_end = Pipe(False)
            proc = Process(target=target, args=(backend.run, text, send_end))
            jobs.append(proc)
            pipe_conns.append(recv_end)
            proc.start()
        for proc in jobs:
            proc.join()
        results = [conn.recv() for conn in pipe_conns]
        return results


core = Core()


def recognize(text: str, config: Config, aggregation_strategy="keep_all", compute_tokens=True) -> dict:
    """Find personally identifiable data in the given text and return it.

    :param compute_tokens:
    :param config:
    :param text:
    :param aggregation_strategy: choose from `keep_all`, `ensure_disjointness` and `merge`
    """
    core.update_config(config)
    results = core.run_recognition(text)

    if len(results) == 0:
        ents = []
    else:
        ents = aggregate(*results, strategy=aggregation_strategy)

    result = {}
    if compute_tokens:
        tokens = core.run_tokenizer(text)
        result["tokens"] = tokens
        add_token_indices(ents, tokens)

    result["ents"] = ents
    return result


def evaluate(ents: List[NamedEntity], gold: List[NamedEntity]) -> dict:
    """Compute the scores of a list of recognized named entities compared to the corresponding true entities.

    Each named entity is required to have the fields `start_char`, `end_char` and `tag` populated. The remaining fields
    are ignored.
    """
    return score_entities(ents, gold)
