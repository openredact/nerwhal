import pytest

from nerwhal import NamedEntity
from nerwhal.aggregation_strategies import aggregate


def test_aggregation():
    ents_a = [
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="spacy_de_core_news_sm")
    ]
    ents_b = [NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re")]
    ents_c = [
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="spacy_de_core_news_sm"
        )
    ]
    assert aggregate(ents_a, ents_b, ents_c) == ents_a + ents_b + ents_c


def test_keep_all_strategy():
    ents = [
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="spacy_de_core_news_sm"),
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="spacy_de_core_news_sm"
        ),
    ]
    assert aggregate(ents, strategy="keep_all") == ents


def test_ensure_disjointness_strategy_with_disjoint_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="spacy_de_core_news_sm"),
        NamedEntity(
            start_char=47, end_char=59, tag="MISC", text="Han's E-Mail", score=0.83, recognizer="spacy_de_core_news_sm"
        ),
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
    ]
    assert aggregate(ents, strategy="ensure_disjointness") == ents


def test_ensure_disjointness_strategy_with_overlapping_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="spacy_de_core_news_sm"),
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="spacy_de_core_news_sm"),
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
    ]
    with pytest.raises(AssertionError):
        aggregate(ents, strategy="ensure_disjointness")


def test_merge_strategy_with_disjoint_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="spacy_de_core_news_sm"),
        NamedEntity(
            start_char=47, end_char=59, tag="MISC", text="Han's E-Mail", score=0.83, recognizer="spacy_de_core_news_sm"
        ),
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
    ]
    assert aggregate(ents, strategy="merge") == ents


def test_merge_strategy_with_overlapping_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="spacy_de_core_news_sm"),
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="spacy_de_core_news_sm"),
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="spacy_de_core_news_sm"),
    ]
    expected_ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="spacy_de_core_news_sm"),
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="spacy_de_core_news_sm"),
    ]
    assert aggregate(ents, strategy="merge") == expected_ents


def test_merge_strategy_with_multiple_overlaps():
    ents = [
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="spacy_de_core_news_sm"),
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="spacy_de_core_news_sm"
        ),
    ]
    expected_ents = [
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
    ]
    assert aggregate(ents, strategy="merge") == expected_ents


def test_merge_strategy_with_multiple_overlaps_highest_score_first():
    ents = [
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="spacy_de_core_news_sm"),
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="spacy_de_core_news_sm"
        ),
    ]
    expected_ents = [
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
    ]
    assert aggregate(ents, strategy="merge") == expected_ents


def test_merge_strategy_with_multiple_overlaps_highest_score_last():
    ents = [
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="spacy_de_core_news_sm"),
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="spacy_de_core_news_sm"
        ),
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
    ]
    expected_ents = [
        NamedEntity(start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="re"),
    ]
    assert aggregate(ents, strategy="merge") == expected_ents
