from typing import Type

from flashtext import KeywordProcessor

from .base import Backend
from nerwhal.types import NamedEntity
from ..recognizer_bases import FlashtextRecognizer


class FlashtextBackend(Backend):
    def __init__(self):
        self.keyword_processor = KeywordProcessor()

    def register_recognizer(self, recognizer_cls: Type[FlashtextRecognizer]):
        recognizer = recognizer_cls()

        key = f"{recognizer.TAG}:{recognizer.SCORE}"
        keyword_dict = {key: recognizer.keywords}
        self.keyword_processor.add_keywords_from_dict(keyword_dict)

    def run(self, text):
        keywords = self.keyword_processor.extract_keywords(text, span_info=True)

        ents = []
        for keyword_key, start, end in keywords:
            tag, score = keyword_key.split(":")
            ent = NamedEntity(start, end, tag, text[start:end], float(score), "flashtext")
            ents.append(ent)
        return ents
