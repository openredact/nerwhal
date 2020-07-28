import csv
import itertools
from pathlib import Path

from nerwhal.recognizer_bases.entity_ruler_recognizer import EntityRulerRecognizer


class DeCountryRecognizer(EntityRulerRecognizer):
    """Recognize German country names in short and long form.

    The long form is also recognized in many declined forms.
    """

    TAG = "LOC"
    SCORE = 0.95

    def __init__(self, nlp):
        super().__init__(nlp)

        one_word_countries = []
        multi_word_countries = []

        for row in self._read_data():
            for name in row:
                if len(name.split()) == 1:
                    # e.g. "Deutschland"
                    one_word_countries.append(name)
                else:
                    # e.g. "Bundesrepublik Deutschland"
                    multi_word_countries.append(name)

        # e.g. [{"LEMMA": "Bundesrepublik"}, {"LEMMA": "Deutschland"}]
        multi_word_patterns = self._compute_multi_word_patterns(multi_word_countries)
        self.country_patterns = list(one_word_countries) + multi_word_patterns

    @property
    def patterns(self):
        return self.country_patterns

    def _read_data(self):
        path = Path(__file__).parent / "data" / "countries.csv"
        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            return list(reader)

    def _compute_multi_word_patterns(self, name_with_multiple_words):
        """Compute several versions of entity ruler patterns for names with multiple words.

        Countries with multiple words aren't matched exactly but by matching against the lemma of each word.
        Frequently, `lemma(a_lemma)` is not the identity function which could matching lemma against lemma fail.
        Thus, we also add the original word to the pattern to catch cases where `lemma(word) == original_word`."""
        multi_word_country_patterns = []
        for name in name_with_multiple_words:
            # (["vereinigt", "Vereinigte"], ["Staat", "Staaten"])
            variants = self._get_variants(name)

            # [("vereinigt", "Staat"), ("vereinigt", "Staaten"), ... ]
            country_name_variants = itertools.product(*variants)

            for variant in country_name_variants:
                multi_word_country_patterns.append([{"LEMMA": sub} for sub in variant])
        print(multi_word_country_patterns)
        return multi_word_country_patterns

    def _get_variants(self, words):
        """Get the lemmas to be able to detect declinations and other variants of country names."""
        result = ()
        for word in words.split():
            # we want word itself to be a variant of word
            variants = [word]

            lemma = self.nlp(word)[0].lemma_
            if lemma != word:
                # the lemma is a version, too
                variants.append(lemma)

            result += (variants,)
        return result
