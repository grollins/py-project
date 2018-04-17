
def convert_column_to_datetime(df, col, fmt='%Y-%m-%d'):
    """Convert dataframe column to datetime"""
    df[col] = pd.to_datetime(my_df[col], format=fmt)
    return df
