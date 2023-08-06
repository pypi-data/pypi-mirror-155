import pandas as pd


def view():
    pd.options.display.float_format = '{:,.2f}'.format  # shows cents!
    return pd.set_option('display.width', None), pd.set_option('display.max_rows', None), \
        pd.set_option('display.max_columns', None), pd.options.display.float_format


def format_cols(df):
    cols = df.columns
    formatted_headers = [x.lower().replace(' ', '_') for x in cols]
    return formatted_headers
