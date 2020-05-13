from pii_identifier import find_piis, evaluate, Pii
from pii_identifier.recognizers.email_recognizer import EmailRecognizer
from pii_identifier.recognizers.spacy_statistical_recognizer import SpacyStatisticalRecognizer


def test_find_piis(embed):
    text = "Han Solo und Wookiee Chewbacca wurden Freunde. Han's E-Mail ist han.solo@imperium.com."
    recognizers = [EmailRecognizer, SpacyStatisticalRecognizer]
    aggregation_strategy = "merge"
    res = find_piis(text, recognizers=recognizers, aggregation_strategy=aggregation_strategy)
    assert embed(text, res["piis"]) == "PER und PER wurden Freunde. MISC ist EMAIL."


def test_evaluate():
    per1 = Pii(0, 5, "PER", "Padme", 1.0, "x")
    per2 = Pii(10, 18, "PER", "Han Solo", 1.0, "x")
    per3 = Pii(14, 18, "PER", "Solo", 1.0, "x")
    loc1 = Pii(20, 25, "LOC", "Naboo", 1.0, "x")
    loc2 = Pii(30, 38, "LOC", "Tatooine", 1.0, "x")
    scores = evaluate([per1, per2, per3, loc1], [per1, per2, loc1, loc2])
    assert scores["total"]["true_positives"] == 3
    assert scores["total"]["false_positives"] == 1
    assert scores["total"]["false_negatives"] == 1
    assert scores["PER"]["true_positives"] == 2
    assert scores["PER"]["false_positives"] == 1
    assert scores["PER"]["false_negatives"] == 0
    assert scores["LOC"]["true_positives"] == 1
    assert scores["LOC"]["false_positives"] == 0
    assert scores["LOC"]["false_negatives"] == 1
