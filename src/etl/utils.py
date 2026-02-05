import pandas as pd

def read(path, header = None):
    return pd.read_excel(path, header = header)


def keep_cols_by_index(data, indices):
    if not all(isinstance(i, int) for i in indices):
        raise TypeError("All column indices must be integers")
    
    if not all(0 <= i < data.shape[1] for i in indices):
        raise IndexError(f"Column index out of range.")
    
    return data.iloc[:,indices].copy()


def drop_na_by_name(data, col_name):
    if isinstance(col_name, str):
        raise TypeError("col_names must be a list of column names, not a string")

    missing = [c for c in col_name if c not in data.columns]
    if missing:
        raise KeyError(f"Missing columns: {missing}")

    return data.dropna(subset=list(col_name)).copy()


def make_columns_numeric(data, cols, er = 'raise'):
    if er not in {"raise", "coerce", "ignore"}:
        raise ValueError("er must be one of: 'raise', 'coerce', 'ignore'")

    if not isinstance(cols,list):
        raise TypeError('cols must be a list of column names')
    
    missing = [c for c in cols if c not in data.columns]
    if missing:
        raise KeyError(f'Missing columns: {missing}')
    
    for c in cols:
        data[c] = pd.to_numeric(data[c], errors = er)

    return data


