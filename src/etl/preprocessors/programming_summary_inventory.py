# Put Rate Manually

import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import drop_rows
from etl.utils import drop_na_by_name
from etl.utils import remove_repeated_headers
from etl.utils import make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,1,2,3,4,5,7,10])
    data.columns = ['Product Code','Product Description','Pur Unit','Qty Pur','Inv Unit','Qty I F','Unit','Avg Cost']
    data = data.iloc[3:-1].copy()
    data = remove_repeated_headers(data,'Product Code')
    data = drop_rows(data,'Product Code',date = True)

    # fill by pattern 
    mask = (
        data['Product Description'].isna() &
        data['Product Description'].shift(-1).isna() &
        data['Product Description'].shift(-2).isna()
        )
    data.loc[mask, 'Category'] = data.loc[mask,'Product Code']
    data['Category'] = data['Category'].ffill()
    data = data[~(data['Category'] == data['Product Code'])].copy()
    data = data.reset_index(drop = True)

    is_nan = data['Product Description'].isna()
    end = is_nan & ~is_nan.shift(-1, fill_value=False)
    ids = data.loc[end].index
    data.loc[ids, 'Group'] = data.loc[ids,'Product Code']
    data['Group'] = data['Group'].ffill()

    data = drop_na_by_name(data,['Product Description'])
    data = data.drop("Product Code", axis=1)
    cols = ['Category','Group','Product Description','Qty I F','Unit','Pur Unit','Qty Pur','Inv Unit','Avg Cost']
    data = data[cols]
    data = make_columns_numeric(data,['Qty I F','Qty Pur','Avg Cost'])
    return data