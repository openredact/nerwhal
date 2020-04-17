from spacy.scorer import PRFScore


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

    return {
        "f1": f1,
        "f2": f2,
        "precision": precision,
        "recall": recall,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }


def score_piis(piis, gold):
    pii_tuples = _to_start_end_type_tuples(piis)
    gold_tuples = _to_start_end_type_tuples(gold)
    types = set([_type for _, _, _type in gold_tuples])

    scores = {"total": score(pii_tuples, gold_tuples)}
    for _type in types:
        scores[_type] = score(_items_with_type(_type, pii_tuples), _items_with_type(_type, gold_tuples))

    return scores


def _to_start_end_type_tuples(piis):
    tuples = [(pii.start, pii.end, pii.type) for pii in piis]
    return tuples


def _items_with_type(_type, start_end_type_tuples):
    return [_tuple for _tuple in start_end_type_tuples if _tuple[2] == _type]


def _fbeta_score(beta, p, r):
    return (1 + beta ** 2) * (p * r) / ((beta ** 2 * p) + r + 1e-100)
