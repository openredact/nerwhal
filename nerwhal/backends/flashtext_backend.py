from typing import Type

from flashtext import KeywordProcessor

from .base import Backend
from nerwhal.types import NamedEntity
from ..recognizer_bases import FlashtextRecognizer


class FlashtextBackend(Backend):
    def __init__(self):
        self.keyword_processors = []
        self.entities = []
        self.score = []

    def register_recognizer(self, recognizer_cls: Type[FlashtextRecognizer]):
        recognizer = recognizer_cls()

        keyword_processor = KeywordProcessor()
        self.keyword_processors.append(keyword_processor.add_keywords_from_list(recognizer.keywords))
        self.entities.append(recognizer.TAG)
        self.score.append(recognizer.SCORE)

    def run(self, text):
        ents = []
        for keyword_processor, entity, score in zip(self.keyword_processors, self.entities, self.score):
            keywords = keyword_processor.extract_keywords(text, span_info=True)
            ents += [NamedEntity(start, end, entity, keyword, score, "flashtext") for keyword, start, end in keywords]
        return ents
