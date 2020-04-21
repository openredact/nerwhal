def aggregate(piis, strategy="keep_all"):
    """

    :param piis: a list of piis
    :param strategy:
    :return:
    """
    piis.sort(key=lambda pii: (pii.start, pii.end, 1.0 - pii.score, pii.type))

    if strategy == "keep_all":
        aggregated = piis
    elif strategy == "only_disjoint":
        aggregated = _only_disjoint_strategy(piis)
    elif strategy == "merge":
        aggregated = _merge_strategy(piis)
    else:
        raise ValueError(f"Unknown aggregation strategy {strategy}")
    return aggregated


def _only_disjoint_strategy(piis):
    # check that all piis are disjunct by comparing end of previous pii with start of the current one
    prev_pii_end = 0
    for pii in piis:
        if prev_pii_end > pii.start:
            raise AssertionError(f"All piis were assumed to be disjunct, but {pii.text} ({pii.start}-{pii.end}) wasn't")

        prev_pii_end = pii.end
    return piis


def _piis_overlap(pii_a, pii_b):
    return pii_a.start <= pii_b.start < pii_a.end or pii_a.start < pii_b.end <= pii_a.end


def _merge_strategy(piis):
    """
    Note, that this might have unwanted results when a group of piis is overlapping
    :param piis:
    :return:
    """
    res = []
    prev_pii = None
    for idx, pii in enumerate(piis):
        next_pii = piis[idx + 1] if idx + 1 < len(piis) else None

        if (
            next_pii
            and _piis_overlap(pii, next_pii)
            and pii.score < next_pii.score
            or prev_pii
            and _piis_overlap(pii, prev_pii)
            and pii.score < prev_pii.score
        ):
            # don't add piis that are overlapping with one that has a higher score
            continue

        res += [pii]
        prev_pii = pii

    return res
