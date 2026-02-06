import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import remove_repeated_headers
from etl.utils import drop_na_by_name
from etl.utils import make_columns_date, make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,4,7,11])
    data.columns = ['Date', 'Location Description', 'Qty', 'Product  Description']
    data = remove_repeated_headers(data,'Date')
    data = drop_na_by_name(data,['Location description'])
    data = drop_na_by_name(data,['qty'])
    data = make_columns_date(data,['Date'])
    data = make_columns_numeric(data,['Qty'])
    return data