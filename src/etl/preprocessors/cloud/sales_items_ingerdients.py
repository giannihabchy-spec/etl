# Price level 1, non separate pages, show cost

import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import remove_repeated_headers
from etl.utils import drop_rows
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,1,3])
    data.columns = ['Product Code', 'Product Description', 'Qty']
    data = remove_repeated_headers(data,'Product Code')
    data = drop_rows(data,'Product Code','Price Level 1')
    data = drop_rows(data,'Product Code',date=True)

    # Clearing 'Product Code' where 'Product Description' exist
    ids = data[~data['Product Description'].isna()].index
    data.loc[ids,'Product Code'] = pd.NA
    # Shift cells up for desc and qty
    data[['Product Description','Qty']] = data[['Product Description','Qty']].shift(-1)
    data['Product Code'] = data['Product Code'].ffill()
    data = drop_na_by_name(data,['Qty'])
    data = make_columns_numeric(data,['Qty'])
    return data