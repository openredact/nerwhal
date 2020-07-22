import pytest

from nerwhal import Pii
from nerwhal.aggregation_strategies import aggregate


def test_aggregation():
    piis_a = [Pii(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, model="spacy_de_core_news_sm")]
    piis_b = [Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re")]
    piis_c = [
        Pii(start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm")
    ]
    assert aggregate(piis_a, piis_b, piis_c) == piis_a + piis_b + piis_c


def test_keep_all_strategy():
    piis = [
        Pii(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm"),
    ]
    assert aggregate(piis, strategy="keep_all") == piis


def test_ensure_disjointness_strategy_with_disjoint_piis():
    piis = [
        Pii(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, model="spacy_de_core_news_sm"),
        Pii(start_char=47, end_char=59, tag="MISC", text="Han's E-Mail", score=0.83, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="ensure_disjointness") == piis


def test_ensure_disjointness_strategy_with_overlapping_piis():
    piis = [
        Pii(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    with pytest.raises(AssertionError):
        aggregate(piis, strategy="ensure_disjointness")


def test_merge_strategy_with_disjoint_piis():
    piis = [
        Pii(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, model="spacy_de_core_news_sm"),
        Pii(start_char=47, end_char=59, tag="MISC", text="Han's E-Mail", score=0.83, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="merge") == piis


def test_merge_strategy_with_overlapping_piis():
    piis = [
        Pii(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, model="spacy_de_core_news_sm"),
    ]
    expected_piis = [
        Pii(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, model="spacy_de_core_news_sm"),
    ]
    assert aggregate(piis, strategy="merge") == expected_piis


def test_merge_strategy_with_multiple_overlaps():
    piis = [
        Pii(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm"),
    ]
    expected_piis = [
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="merge") == expected_piis


def test_merge_strategy_with_multiple_overlaps_highest_score_first():
    piis = [
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
        Pii(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm"),
    ]
    expected_piis = [
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="merge") == expected_piis


def test_merge_strategy_with_multiple_overlaps_highest_score_last():
    piis = [
        Pii(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, model="spacy_de_core_news_sm"),
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    expected_piis = [
        Pii(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, model="re"),
    ]
    assert aggregate(piis, strategy="merge") == expected_piis
