from typing import List

from spacy.scorer import PRFScore

from pii_identifier import Pii, Score


def score(candidates, gold):
    prf_scorer = PRFScore()
    prf_scorer.score_set(set(candidates), set(gold))

    f1 = prf_scorer.fscore
    f2 = _fbeta_score(2, prf_scorer.precision, prf_scorer.recall)
    precision = prf_scorer.precision
    recall = prf_scorer.recall
    true_positives = prf_scorer.tp
    false_positives = prf_scorer.fp
    false_negatives = prf_scorer.fn

    return Score(f1, f2, precision, recall, true_positives, false_positives, false_negatives)


def score_piis(piis: List[Pii], gold: List[Pii]):
    return score(_to_start_end_type_tuples(piis), _to_start_end_type_tuples(gold))


def _to_start_end_type_tuples(piis):
    tuples = [(pii.start, pii.end, pii.type) for pii in piis]
    return tuples


def _fbeta_score(beta, p, r):
    return (1 + beta ** 2) * (p * r) / ((beta ** 2 * p) + r + 1e-100)
