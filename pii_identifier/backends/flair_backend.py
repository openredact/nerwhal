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
    def __init__(self):
        self.active = False

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
        pos_shift = 0
        for sentence in sentences:
            piis += [
                Pii(
                    ent.start_pos + pos_shift,
                    ent.end_pos + pos_shift,
                    _align_tags(ent.tag),
                    ent.text,
                    ent.score,
                    "flair_" + MODEL,
                )
                for ent in sentence.get_spans("ner")
            ]
            pos_shift += len(sentence.to_original_text()) + 1  # 1 for the space/newline after the sentence terminal

        return piis


def _align_tags(tag):
    if tag == "OTH":
        return "MISC"
    else:
        return tag
