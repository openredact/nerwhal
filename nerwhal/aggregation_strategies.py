def aggregate(ents, *other_ents, strategy="keep_all"):
    """Aggregate two or more lists of named entities.

    You can choose from several strategies for how to deal with overlapping entities.
    - `keep_all`: Append all lists and keep all entities.
    - `ensure_disjointness`: Like `keep_all`, but raises an `AssertionError` if two entities overlap.
    - `merge`: Appends the lists while choosing the entity with higher score on overlaps.
    """
    items = ents.copy()
    for _ents in other_ents:
        items.extend(_ents)

    items.sort(key=lambda ent: (ent.start_char, ent.end_char, 1.0 - ent.score, ent.tag))

    if strategy == "keep_all":
        aggregated = items
    elif strategy == "ensure_disjointness":
        aggregated = _ensure_disjointness_strategy(items)
    elif strategy == "merge":
        aggregated = _merge_strategy(items)
    else:
        raise ValueError(f"Unknown aggregation strategy {strategy}")
    return aggregated


def _ensure_disjointness_strategy(ents):
    """A strategy that ensures that all entities are disjoint.

    Checks that all entities are disjoint by comparing end of previous entity with start of the current one.
    """
    prev_ent_end = 0
    for ent in ents:
        if prev_ent_end > ent.start_char:
            raise AssertionError(
                f"All entities were assumed to be disjunct, but {ent.text} ({ent.start_char}-{ent.end_char}) wasn't"
            )

        prev_ent_end = ent.end_char
    return ents


def _overlapping(ent_a, ent_b):
    return ent_a.start_char <= ent_b.start_char < ent_a.end_char or ent_a.start_char < ent_b.end_char <= ent_a.end_char


def _overlapping_and_outscored(ent, other_ent):
    return other_ent and _overlapping(ent, other_ent) and ent.score < other_ent.score


def _merge_strategy(ents):
    """A strategy to resolve overlapping named entities by giving those with higher scores priority."""
    res = []
    prev_ent = None
    for idx, ent in enumerate(ents):
        next_ent = ents[idx + 1] if idx + 1 < len(ents) else None

        if _overlapping_and_outscored(ent, prev_ent) or _overlapping_and_outscored(ent, next_ent):
            # don't add this one
            continue

        res += [ent]

        prev_ent = ent

    return res
