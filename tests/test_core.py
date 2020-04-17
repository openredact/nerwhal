from pii_identifier import evaluate, Pii


def test_find_piis():
    pass


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
