import pytest

from nerwhal import recognize, evaluate, NamedEntity, Config
from nerwhal.types import Token


def test_recognize(embed):
    text = "Die E-Mail von Han ist han.solo@imperium.com."
    config = Config("de", recognizer_paths=["nerwhal/integrated_recognizers/email_recognizer.py"])
    res = recognize(text, config=config, combination_strategy="fusion")
    assert embed(text, res["ents"]) == "Die E-Mail von Han ist EMAIL."
    assert res["tokens"][0] == Token(text="Die", has_ws=True, br_count=0, start_char=0, end_char=3)


@pytest.mark.stanza
def test_recognize_with_statistical_ner(embed):
    text = "Han Solo und Wookiee Chewbacca wurden Freunde. Die E-Mail von Han ist han.solo@imperium.com."
    config = Config("de", use_statistical_ner=True, recognizer_paths=["nerwhal/integrated_recognizers/email_recognizer.py"])
    res = recognize(text, config=config, combination_strategy="fusion")
    assert embed(text, res["ents"]) == "PER und PER wurden Freunde. Die E-Mail von PER ist EMAIL."
    assert res["tokens"][0] == Token(text="Han", has_ws=True, br_count=0, start_char=0, end_char=3)


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


def test_boosting_confidence_with_context_words(embed):
    config = Config("de", recognizer_paths=["nerwhal/integrated_recognizers/de/de_date_recognizer.py"])

    text_with_context = "Ich habe am 12.12.2012 Geburtstag."
    res_with_context = recognize(text_with_context, config=config, context_words=True)
    assert embed(text_with_context, res_with_context["ents"]) == "Ich habe am DATE Geburtstag."

    text_without_context = "Ich habe am 12.12.2012 Hunger."
    res_without_context = recognize(text_without_context, config=config, context_words=True)
    assert embed(text_without_context, res_without_context["ents"]) == "Ich habe am DATE Hunger."

    assert res_with_context["ents"][0].score > res_without_context["ents"][0].score
