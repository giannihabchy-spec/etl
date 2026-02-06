# All Branches

import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import drop_na_by_name
from etl.utils import remove_repeated_headers
from etl.utils import make_columns_date, make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[1,4,5,6,7,13])
    data.columns = ['Location','Supplier','Purchase Date','Invoice #','Product Description','Total']
    data = drop_na_by_name(data,['Invoice #'])
    data = remove_repeated_headers(data,'Location')
    data = make_columns_numeric(data,['Total'])
    data = make_columns_date(data,['Purchase Date'])
    cols = ['Location','Product Description','Total','Supplier','Invoice #','Purchase Date']
    data = data[cols]
    return data