from pandas import to_datetime


def convert_series_to_datetime(s, fmt='%Y-%m-%d'):
    """Convert series to datetime"""
    return to_datetime(s, format=fmt)
