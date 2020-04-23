def aggregate(piis, *other_piis, strategy="keep_all"):
    """Aggregate two or more lists of Piis.

    You can choose from several strategies for how to deal with overlapping Piis.
    - `keep_all`: Append all lists and keep all Piis.
    - `ensure_disjointness`: Like `keep_all`, but raises an `AssertionError` if two Piis overlap.
    - `merge`: Appends the lists while choosing the Pii with higher score on overlaps.
    """
    items = piis.copy()
    for _piis in other_piis:
        items.extend(_piis)

    items.sort(key=lambda pii: (pii.start, pii.end, 1.0 - pii.score, pii.type))

    if strategy == "keep_all":
        aggregated = items
    elif strategy == "ensure_disjointness":
        aggregated = _ensure_disjointness_strategy(items)
    elif strategy == "merge":
        aggregated = _merge_strategy(items)
    else:
        raise ValueError(f"Unknown aggregation strategy {strategy}")
    return aggregated


def _ensure_disjointness_strategy(piis):
    """A strategy that ensures that all PIIs are disjoint.

    Checks that all piis are disjoint by comparing end of previous pii with start of the current one.
    """
    prev_pii_end = 0
    for pii in piis:
        if prev_pii_end > pii.start:
            raise AssertionError(f"All piis were assumed to be disjunct, but {pii.text} ({pii.start}-{pii.end}) wasn't")

        prev_pii_end = pii.end
    return piis


def _overlapping(pii_a, pii_b):
    return pii_a.start <= pii_b.start < pii_a.end or pii_a.start < pii_b.end <= pii_a.end


def _overlapping_and_outscored(pii, other_pii):
    return other_pii and _overlapping(pii, other_pii) and pii.score < other_pii.score


def _merge_strategy(piis):
    """A strategy to resolve overlapping PIIs by giving those with higher scores priority."""
    res = []
    prev_pii = None
    for idx, pii in enumerate(piis):
        next_pii = piis[idx + 1] if idx + 1 < len(piis) else None

        if _overlapping_and_outscored(pii, prev_pii) or _overlapping_and_outscored(pii, next_pii):
            # don't add this one
            continue

        res += [pii]

        prev_pii = pii

    return res
