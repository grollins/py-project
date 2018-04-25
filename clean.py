from numpy import nan
from pandas import to_datetime
from fuzzywuzzy import process


def convert_series_to_datetime(s, fmt='%Y-%m-%d'):
    """Convert series to datetime"""
    return to_datetime(s, format=fmt)

def fuzzy_match(s, choices, score_cutoff=80):
    """Fuzzy match string to list of possible values"""
    m = process.extractOne(s, choices=choices, score_cutoff=score_cutoff)
    if m:
        return m[0]
    else:
        return nan
