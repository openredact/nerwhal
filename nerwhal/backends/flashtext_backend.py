from flashtext import KeywordProcessor

from nerwhal import Pii
from nerwhal.backends.base import Backend


class FlashtextBackend(Backend):
    def __init__(self):
        self.keyword_processors = []
        self.entities = []
        self.precisions = []

    def register_recognizer(self, recognizer):
        keyword_processor = KeywordProcessor()
        self.keyword_processors.append(keyword_processor.add_keywords_from_list(recognizer.keywords))
        self.entities.append(recognizer.entity)
        self.precisions.append(recognizer.precision)

    def run(self, text):
        piis = []
        for keyword_processor, entity, precision in zip(self.keyword_processors, self.entities, self.precisions):
            keywords = keyword_processor.extract_keywords(text, span_info=True)
            piis += [Pii(start, end, entity, keyword, precision, "flashtext") for keyword, start, end in keywords]
        return piis
