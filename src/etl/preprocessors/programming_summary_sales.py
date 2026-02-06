# All Branches

import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import remove_repeated_headers
from etl.utils import drop_rows
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,1,4])
    data.columns = ['Nbr','Description','Price Level 1']
    data = remove_repeated_headers(data,'Description')
    data = drop_rows(data,'Nbr',date=True)
    data = drop_rows(data,'Nbr','Item ID')
    data['Nbr'] = data['Nbr'].shift(-1)
    data = drop_na_by_name(data,['Nbr'])

    # Category
    mask = (
    data['Description'].isna() &
    data['Description'].shift(-1).isna() &
    data['Description'].shift(-2).isna()
    )
    data.loc[mask, 'Category'] = data.loc[mask, 'Nbr']
    data['Category'] = data['Category'].ffill()

    data = data.reset_index(drop = True)

    is_nan = data['Description'].isna()
    end = is_nan & ~is_nan.shift(-1, fill_value=False)
    ids = data.loc[end].index

    # Group
    data.loc[ids,'Group'] = data.loc[ids,'Nbr']
    data['Group'] = data['Group'].ffill()

    data = drop_na_by_name(data,['Description'])

    cols = ['Category','Group','Description','Price Level 1']
    data = data[cols]

    data = make_columns_numeric(data,['Price Level 1'])
    return data