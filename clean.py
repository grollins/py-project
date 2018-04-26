from numpy import nan
from pandas import to_datetime, to_numeric
from fuzzywuzzy import process


def convert_series_to_datetime(srs, fmt='%Y-%m-%d'):
    """Convert series to datetime"""
    return to_datetime(srs, format=fmt)

def convert_series_to_numeric(srs):
    """Convert series to numeric. Coerce strings to NaN."""
    return to_numeric(srs, errors='coerce')

def fuzzy_match(s, choices, score_cutoff=80):
    """Fuzzy match string to list of possible values.
    Based on http://pbpython.com/excel-pandas-comp.html
    """
    m = process.extractOne(s, choices=choices, score_cutoff=score_cutoff)
    if m:
        return m[0]
    else:
        return nan

def convert_currency(s):
    """
    Convert the string number value to a float
     - Remove $
     - Remove commas
     - Convert to float type
    http://pbpython.com/pandas_dtypes.html
    """
    new_s = s.replace(',','').replace('$', '')
    return float(new_s)

def convert_percent(s):
    """
    Convert the percentage string to an actual floating point percent
    - Remove %
    - Divide by 100 to make decimal
    http://pbpython.com/pandas_dtypes.html
    """
    new_s = s.replace('%', '')
    return float(new_s) / 100

def convert_binary_choice_string_to_bool(s, true_str=None):
    """
    Convert string to boolean
     - If string matches one of the True values, return True
     - Else return False
     - If no True values are provided, return NaN
    """
    if true_str:
        return s in true_str
    else:
        return nan

def aggregate_over_time_freq(df, group_col='group', dt_col='date', freq='M',
                             value_col='count'):
    """
    Sum values by group over a given time frequency, e.g. monthly
    http://pbpython.com/pandas-grouper-agg.html
    http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
    """
    g = pd.Grouper(key=dt_col, freq=freq)
    return df.groupby([group_col, g])[value_col].sum()

def do_agg(df, cols, agg_fcn=None):
    """
    Apply aggregation functions to given columns of a dataframe
    http://pbpython.com/pandas-grouper-agg.html
    """
    if agg_fcn is None:
        agg_fcn = ['sum', 'mean']
    return df[cols].agg(agg_fcn)

def compute_pct_by_group(df, group_col='group', value_col='count'):
    """
    Determine what percent each element contributes to its group's total.
      - Sum value by group to get group totals
      - Divide each group element by its group's total to get fraction of group
      - Multiply by 100 to get percent of group for each group element
      - Return series with percent-of-group values
    http://pbpython.com/pandas_transform.html
    """
    total = df.groupby(group_col)[value_col].transform('sum')
    return df[value_col] / total * 100.
