import csv
from pathlib import Path

from nerwhal.recognizer_bases.flashtext_recognizer import FlashtextRecognizer


class DeCountryRecognizer(FlashtextRecognizer):
    """Recognize German country names in short and long form.

    This recognizer searches for occurrences of German country names, loaded from a file. Thus, what it can find is limited by
    the completeness of the data in this file. Our data file also contains many declined versions of the long form of country
    names, that can then be recognized as well.
    """

    TAG = "COUNTRY"
    SCORE = 0.95
    CONTEXT_WORDS = ["Land", "Länder", "Staat", "Staaten"]

    def __init__(self):
        path = Path(__file__).parent / "data" / "countries.csv"
        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            self.country_names = [name for row in reader for name in row]

    @property
    def keywords(self):
        return self.country_names
