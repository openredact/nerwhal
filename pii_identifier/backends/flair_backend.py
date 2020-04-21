import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    from flair.data import Sentence
    from flair.models import SequenceTagger
    from segtok.segmenter import split_single

from pii_identifier import Pii  # noqa: E402
from pii_identifier.backends.backend_base import NlpBackend  # noqa: E402
from pii_identifier.recognizers.flair_statistical_recognizer import FlairStatisticalRecognizer  # noqa: E402

MODEL = "de-ner-germeval"  # Germeval,  84.90 F1

tagger = SequenceTagger.load(MODEL)


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
                Pii(ent.start_pos, ent.end_pos, _align_tags(ent.tag), ent.text, ent.score, "flair_" + MODEL)
                for ent in sentence.get_spans("ner")
            ]

        return piis


def _align_tags(tag):
    if tag == "OTH":
        return "MISC"
    else:
        return tag
