import csv
from pathlib import Path

from nerwhal.recognizer_bases.flashtext_recognizer import FlashtextRecognizer


class DeCountryRecognizer(FlashtextRecognizer):
    """Recognize German country names in short and long form.

    The long form is also recognized in many declined forms.
    """

    TAG = "LOC"
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
