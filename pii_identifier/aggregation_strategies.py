def aggregate(piis, *other_piis, strategy="keep_all"):
    # other strategies may include:
    # - merge: if piis of different type overlap keep the one with higher score, if they are of same type combine
    # - rigid: raise an error if piis overlap
    # maybe flags are handy too:
    # - rescore: if a pii is found twice, combine the scores

    if strategy == "keep_all":
        [piis.extend(other) for other in other_piis]
    else:
        raise ValueError(f"Unknown aggregation strategy {strategy}")
    return piis
