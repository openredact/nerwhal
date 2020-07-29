from nerwhal import recognize, evaluate, NamedEntity, Config


def test_recognize(embed):
    text = "Han Solo und Wookiee Chewbacca wurden Freunde. Die E-Mail von Han ist han.solo@imperium.com."
    config = Config("de", use_statistical_ner=True, recognizer_paths=["nerwhal/example_recognizers/email_recognizer.py"])
    res = recognize(text, config=config, aggregation_strategy="merge")
    assert embed(text, res["ents"]) == "PER und PER wurden Freunde. Die E-Mail von PER ist EMAIL."


def test_evaluate():
    per1 = NamedEntity(0, 5, "PER", "Padme", 1.0, "x")
    per2 = NamedEntity(10, 18, "PER", "Han Solo", 1.0, "x")
    per3 = NamedEntity(14, 18, "PER", "Solo", 1.0, "x")
    loc1 = NamedEntity(20, 25, "LOC", "Naboo", 1.0, "x")
    loc2 = NamedEntity(30, 38, "LOC", "Tatooine", 1.0, "x")
    scores = evaluate([per1, per2, per3, loc1], [per1, per2, loc1, loc2])
    assert scores["total"]["true_positives"] == 3
    assert scores["total"]["false_positives"] == 1
    assert scores["total"]["false_negatives"] == 1
    assert scores["tags"]["PER"]["true_positives"] == 2
    assert scores["tags"]["PER"]["false_positives"] == 1
    assert scores["tags"]["PER"]["false_negatives"] == 0
    assert scores["tags"]["LOC"]["true_positives"] == 1
    assert scores["tags"]["LOC"]["false_positives"] == 0
    assert scores["tags"]["LOC"]["false_negatives"] == 1
