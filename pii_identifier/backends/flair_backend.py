from flair.data import Sentence
from flair.models import SequenceTagger
from segtok.segmenter import split_single

from pii_identifier import PII
from pii_identifier.backends.backend_base import NlpBackend
from pii_identifier.recognizers.flair_statistical_recognizer import FlairStatisticalRecognizer

MODEL = "de-ner-germeval"  # Germeval,  84.90 F1

tagger = SequenceTagger.load(MODEL)

# TODO mute flair import warnings


class FlairBackend(NlpBackend):
    active = False

    def register_recognizer(self, recognizer):
        if isinstance(recognizer, FlairStatisticalRecognizer):
            self.active = True
        else:
            raise TypeError(f"Trying to register recognizer with unsupported type {type(recognizer)}")

    def run(self, text):
        assert self.active

        sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)]
        tagger.predict(sentences)

        piis = []
        for sentence in sentences:  # TODO multiple sentences require a pos shift
            piis += [
                PII(ent.start_pos, ent.end_pos, _align_tags(ent.tag), ent.text, ent.score, "flair_ner_multi_fast")
                for ent in sentence.get_spans("ner")
            ]

        return piis


def _align_tags(tag):
    if tag == "OTH":
        return "MISC"
    else:
        return tag
