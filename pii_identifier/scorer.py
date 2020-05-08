from spacy.scorer import PRFScore


def score(candidates, gold):
    """Compute the most common scoring measures for any two sets.

    :param candidates: the candidates to be scored; the predicted values
    :param gold: the true values
    :return: a dictionary with the scores
    """

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
    """Compute a range of scores for a list of piis compared to the true piis contained in the text.

    :param piis: a list of piis, as returned by `pii_identifier.find_piis`
    :param gold: the true list of piis
    :return: a dictionary with the scores
    """
    pii_tuples = _to_start_end_tag_tuples(piis)
    gold_tuples = _to_start_end_tag_tuples(gold)
    tags = set([tag for _, _, tag in gold_tuples])

    scores = {"total": score(pii_tuples, gold_tuples)}
    for tag in tags:
        scores[tag] = score(_items_with_tag(tag, pii_tuples), _items_with_tag(tag, gold_tuples))

    return scores


def _to_start_end_tag_tuples(piis):
    tuples = [(pii.start, pii.end, pii.tag) for pii in piis]
    return tuples


def _items_with_tag(tag, start_end_tag_tuples):
    return [_tuple for _tuple in start_end_tag_tuples if _tuple[2] == tag]


def _fbeta_score(beta, p, r):
    return (1 + beta ** 2) * (p * r) / ((beta ** 2 * p) + r + 1e-100)
