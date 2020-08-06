def combine(ents, *other_ents, strategy="append"):
    """Combine two or more lists of named entities.

    You can choose from several strategies for how to deal with overlapping entities.
    - `append`: Append all lists of entities.
    - `disjunctive_union`: The disjunctive union of all entities. This assumes the lists to be disjunct;
        an error is thrown if two entities overlap.
    - `fusion`: Appends the lists while choosing the entity with higher score on overlaps.
    - `smart-fusion`: Like fusion, but add scores if entities were identified multiple times.
    """
    items = ents.copy()
    for _ents in other_ents:
        items.extend(_ents)

    items.sort(key=lambda ent: (ent.start_char, ent.end_char, 1.0 - ent.score, ent.tag))

    if strategy == "append":
        combined = items
    elif strategy == "disjunctive_union":
        combined = _disjunctive_union_strategy(items)
    elif strategy == "fusion":
        combined = _fusion_strategy(items)
    elif strategy == "smart-fusion":
        combined = _smart_fusion_strategy(items)
    else:
        raise ValueError(f"Unknown aggregation strategy {strategy}")
    return combined


def _disjunctive_union_strategy(ents):
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


def _overlapping_with_same_score_but_shorter(ent, other_ent):
    return (
        other_ent
        and _overlapping(ent, other_ent)
        and ent.score == other_ent.score
        and ent.end_tok - ent.start_tok < other_ent.end_tok - other_ent.start_tok
    )


def _fusion_strategy(ents):
    """A strategy to resolve overlapping named entities by giving those with higher scores priority."""
    res = []
    prev_ent = None
    for idx, ent in enumerate(ents):
        next_ent = ents[idx + 1] if idx + 1 < len(ents) else None

        if (
            _overlapping_and_outscored(ent, prev_ent)
            or _overlapping_and_outscored(ent, next_ent)
            or _overlapping_with_same_score_but_shorter(ent, prev_ent)
            or _overlapping_with_same_score_but_shorter(ent, next_ent)
        ):
            # don't add this one
            continue

        res += [ent]
        prev_ent = ent

    return res


def _is_same(ent_a, ent_b):
    return ent_a.start_char == ent_b.start_char and ent_a.end_char == ent_b.end_char and ent_a.tag == ent_b.tag


def _smart_fusion_strategy(ents):
    deduplicated_ents = []
    for idx, ent in enumerate(ents):
        next_ent = ents[idx + 1] if idx + 1 < len(ents) else None

        if next_ent and _is_same(next_ent, ent):
            next_ent.score = min(next_ent.score + ent.score, 1.0)
            continue

        deduplicated_ents.append(ent)

    return _fusion_strategy(deduplicated_ents)
