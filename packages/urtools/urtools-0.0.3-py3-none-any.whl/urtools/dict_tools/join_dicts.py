def join_dicts(*dicts: dict) -> dict:
    joined = {}
    for d in dicts:
        joined.update(d)
    return joined
