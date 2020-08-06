import pytest

from nerwhal import NamedEntity
from nerwhal.combination_strategies import combine


def test_interface():
    ents_a = [NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="SomeRecognizer")]
    ents_b = [
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        )
    ]
    ents_c = [
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="SomeRecognizer"
        )
    ]
    assert combine(ents_a, ents_b, ents_c) == ents_a + ents_b + ents_c


def test_append_strategy():
    ents = [
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="SomeRecognizer"
        ),
    ]
    assert combine(ents, strategy="append") == ents


def test_disjunctive_union_strategy_with_disjoint_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(start_char=47, end_char=59, tag="MISC", text="Han's E-Mail", score=0.83, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
    ]
    assert combine(ents, strategy="disjunctive_union") == ents


def test_disjunctive_union_strategy_with_overlapping_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
    ]
    with pytest.raises(AssertionError):
        combine(ents, strategy="disjunctive_union")


def test_fusion_strategy_with_disjoint_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(start_char=47, end_char=59, tag="MISC", text="Han's E-Mail", score=0.83, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
    ]
    assert combine(ents, strategy="fusion") == ents


def test_fusion_strategy_with_overlapping_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    expected_ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    assert combine(ents, strategy="fusion") == expected_ents


def test_fusion_strategy_with_multiple_overlaps():
    ents = [
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="SomeRecognizer"
        ),
    ]
    expected_ents = [
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
    ]
    assert combine(ents, strategy="fusion") == expected_ents


def test_fusion_strategy_with_multiple_overlaps_highest_score_first():
    ents = [
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="SomeRecognizer"
        ),
    ]
    expected_ents = [
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
    ]
    assert combine(ents, strategy="fusion") == expected_ents


def test_fusion_strategy_with_multiple_overlaps_highest_score_last():
    ents = [
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="ORG", text="han.solo@imperium.com", score=0.83, recognizer="SomeRecognizer"
        ),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
    ]
    expected_ents = [
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
    ]
    assert combine(ents, strategy="fusion") == expected_ents


def test_fusion_with_same_score_overlapping():
    ents = [
        NamedEntity(
            start_char=301,
            end_char=306,
            tag="PHONE",
            text="12345",
            score=0.8,
            recognizer="AnotherRecognizer",
            start_tok=44,
            end_tok=45,
        ),
        NamedEntity(
            start_char=301,
            end_char=313,
            tag="LOC",
            text="12345 Berlin",
            score=0.8,
            recognizer="AnotherRecognizer",
            start_tok=44,
            end_tok=46,
        ),
    ]
    expected_ents = [
        NamedEntity(
            start_char=301,
            end_char=313,
            tag="LOC",
            text="12345 Berlin",
            score=0.8,
            recognizer="AnotherRecognizer",
            start_tok=44,
            end_tok=46,
        ),
    ]
    assert combine(ents, strategy="fusion") == expected_ents


def test_smart_fusion_strategy_with_disjoint_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(start_char=47, end_char=59, tag="MISC", text="Han's E-Mail", score=0.83, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
    ]
    assert combine(ents, strategy="smart-fusion") == ents


def test_smart_fusion_strategy_with_overlapping_ents():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.92, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    expected_ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    assert combine(ents, strategy="smart-fusion") == expected_ents


def test_smart_fusion_strategy_with_double_match():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=0.92, recognizer="SomeRecognizer"
        ),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=0.5, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    expected_ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    assert combine(ents, strategy="smart-fusion") == expected_ents


def test_smart_fusion_strategy_with_triple_match():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=0.92, recognizer="SomeRecognizer"
        ),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=0.5, recognizer="AnotherRecognizer"
        ),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=0.5, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    expected_ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    assert combine(ents, strategy="smart-fusion") == expected_ents


def test_smart_fusion_strategy_with_double_match_and_overlap():
    ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(start_char=64, end_char=71, tag="MISC", text="han.solo", score=0.99, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=0.5, recognizer="SomeRecognizer"
        ),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=0.5, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    expected_ents = [
        NamedEntity(start_char=0, end_char=8, tag="PER", text="Han Solo", score=0.94, recognizer="SomeRecognizer"),
        NamedEntity(
            start_char=64, end_char=85, tag="EMAIL", text="han.solo@imperium.com", score=1.0, recognizer="AnotherRecognizer"
        ),
        NamedEntity(start_char=100, end_char=108, tag="LOC", text="Tatooine", score=0.98, recognizer="SomeRecognizer"),
    ]
    assert combine(ents, strategy="smart-fusion") == expected_ents
