def filter_dict_nans(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None and v == v and str(v).lower() != 'nan'}

def dict_has_nans(d: dict) -> bool:
    return any(v for v in d.values() if v is None or v != v or str(v).lower() == 'nan')
