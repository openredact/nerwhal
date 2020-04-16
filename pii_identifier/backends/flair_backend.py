from flair.data import Sentence
from flair.models import SequenceTagger
from segtok.segmenter import split_single

from pii_identifier import PII
from pii_identifier.backends.backend_base import NlpBackend
from pii_identifier.recognizers.flair_statistical_recognizer import FlairStatisticalRecognizer

MODEL = "ner-multi-fast"  # Conll-03 (English, German, Dutch and Spanish),  87.91 average F1

tagger = SequenceTagger.load(MODEL)


class FlairBackend(NlpBackend):
    active = False

    def register_recognizer(self, recognizer):
        if isinstance(recognizer, FlairStatisticalRecognizer):
            self.active = True
        else:
            raise TypeError(f"Trying to register recognizer with unsupported type {type(recognizer)}")

    def run(self, text):
        if not self.active:
            return

        sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
        tagger.predict(sentences)

        piis = []
        for sentence in sentences:
            piis += [
                PII(ent.start_pos, ent.end_pos, ent.tag, ent.text, ent.score, "flair_ner_multi_fast")
                for ent in sentence.get_spans("ner")
            ]

        return piis
