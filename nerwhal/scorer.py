from spacy.scorer import PRFScore


def score_entities(candidates, gold):
    """Compute a range of scores for a list of named entities compared to the true entities contained in the text.

    :param candidates: a list of named entities, with at least have the properties `start_char`, `end_char`, and `tag`
    :param gold: the true list of named entities, with at least have the properties `start_char`, `end_char`, and `tag`
    :return: a dictionary with the scores
    """
    cand_tuples = _to_start_end_tag_tuples(candidates)
    gold_tuples = _to_start_end_tag_tuples(gold)
    tags = set([tag for _, _, tag in gold_tuples + cand_tuples])

    scores = {"total": score(cand_tuples, gold_tuples), "tags": {}}
    for tag in tags:
        scores["tags"][tag] = score(_select_tuples_with_tag(tag, cand_tuples), _select_tuples_with_tag(tag, gold_tuples))

    return scores


def score(candidates, gold):
    """Compute the most common scoring measures for any two sets.

    :param candidates: the candidates to be scored, i.e. the predicted values
    :param gold: the true values
    :return: a dictionary with the scores
    """

    prf_scorer = PRFScore()
    prf_scorer.score_set(set(candidates), set(gold))

    return {
        "f1": prf_scorer.fscore,
        "f2": _fbeta_score(2, prf_scorer.precision, prf_scorer.recall),
        "precision": prf_scorer.precision,
        "recall": prf_scorer.recall,
        "true_positives": prf_scorer.tp,
        "false_positives": prf_scorer.fp,
        "false_negatives": prf_scorer.fn,
    }


def _to_start_end_tag_tuples(ents):
    tuples = [(ent.start_char, ent.end_char, ent.tag) for ent in ents]
    return tuples


def _select_tuples_with_tag(tag, start_end_tag_tuples):
    return [_tuple for _tuple in start_end_tag_tuples if _tuple[2] == tag]


def _fbeta_score(beta, p, r):
    """Compute the F-beta score for a given precision and recall."""
    return (1 + beta ** 2) * (p * r) / ((beta ** 2 * p) + r + 1e-100)
