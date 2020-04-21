import pytest

from pii_identifier import Pii
from pii_identifier.aggregation_strategies import aggregate


def test_keep_all_strategy():
    piis = [
        Pii(start=64, end=71, type="MISC", text="han.solo", score=0.92, model="flair_ner_multi_fast"),
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start=64, end=85, type="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm"),
    ]
    assert aggregate(piis, strategy="keep_all") == piis


def test_only_disjoint_strategy_with_disjoint_piis():
    piis = [
        Pii(start=0, end=8, type="PER", text="Han Solo", score=0.94, model="flair_ner_multi_fast"),
        Pii(start=47, end=59, type="MISC", text="Han's E-Mail", score=0.83, model="spacy_de_core_news_sm"),
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="only_disjoint") == piis


def test_only_disjoint_strategy_with_overlapping_piis():
    piis = [
        Pii(start=0, end=8, type="PER", text="Han Solo", score=0.94, model="flair_ner_multi_fast"),
        Pii(start=64, end=71, type="MISC", text="han.solo", score=0.92, model="flair_ner_multi_fast"),
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    with pytest.raises(AssertionError):
        aggregate(piis, strategy="only_disjoint")


def test_merge_strategy_with_disjoint_piis():
    piis = [
        Pii(start=0, end=8, type="PER", text="Han Solo", score=0.94, model="flair_ner_multi_fast"),
        Pii(start=47, end=59, type="MISC", text="Han's E-Mail", score=0.83, model="spacy_de_core_news_sm"),
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="merge") == piis


def test_merge_strategy_with_overlapping_piis():
    piis = [
        Pii(start=0, end=8, type="PER", text="Han Solo", score=0.94, model="flair_ner_multi_fast"),
        Pii(start=64, end=71, type="MISC", text="han.solo", score=0.92, model="flair_ner_multi_fast"),
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start=100, end=108, type="LOC", text="Tatooine", score=0.98, model="flair_ner_multi_fast"),
    ]
    expected_piis = [
        Pii(start=0, end=8, type="PER", text="Han Solo", score=0.94, model="flair_ner_multi_fast"),
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start=100, end=108, type="LOC", text="Tatooine", score=0.98, model="flair_ner_multi_fast"),
    ]
    assert aggregate(piis, strategy="merge") == expected_piis


def test_merge_strategy_with_multiple_overlaps():
    piis = [
        Pii(start=64, end=71, type="MISC", text="han.solo", score=0.92, model="flair_ner_multi_fast"),
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start=64, end=85, type="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm"),
    ]
    expected_piis = [
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="merge") == expected_piis


def test_merge_strategy_with_multiple_overlaps_highest_score_first():
    piis = [
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start=64, end=71, type="MISC", text="han.solo", score=0.92, model="flair_ner_multi_fast"),
        Pii(start=64, end=85, type="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm"),
    ]
    expected_piis = [
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="merge") == expected_piis


def test_merge_strategy_with_multiple_overlaps_highest_score_last():
    piis = [
        Pii(start=64, end=71, type="MISC", text="han.solo", score=0.92, model="flair_ner_multi_fast"),
        Pii(start=64, end=85, type="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm"),
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    expected_piis = [
        Pii(start=64, end=85, type="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="merge") == expected_piis
