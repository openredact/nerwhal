import pytest

from pii_identifier.scorer import score


def test_f1():
    res = score([1, 2], [1, 2, 3])
    assert res.f1 == pytest.approx(0.8)


def test_f2():
    # the b in fb-score determines the weight of recall
    res = score([1, 2], [1, 2, 3])
    assert res.f2 < res.f1  # (p=1.0, r=0.66)


def test_precision():
    res = score([1, 2, 3], [1, 2])
    assert res.precision == pytest.approx(0.66, 0.1)


def test_recall():
    res = score([1, 2], [1, 2, 3])
    assert res.recall == pytest.approx(0.66, 0.1)


def test_true_positives():
    res = score([1, 2, 4], [1, 2, 3])
    assert res.true_positives == 2


def test_false_positives():
    res = score([1, 2, 4], [1, 2, 3])
    assert res.false_positives == 1


def test_false_negatives():
    res = score([1, 2, 4], [1, 2, 3])
    assert res.false_negatives == 1
