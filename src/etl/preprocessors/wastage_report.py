import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import remove_repeated_headers
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric, make_columns_date


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,3,4,10,13])
    data.columns = ['Qty', 'Product Description', 'Remark', 'Date', 'Location']
    data = drop_na_by_name(data,['Product Description'])
    data = remove_repeated_headers(data,'Qty')
    cols = ['Location','Qty','Product Description','Remark','Date']
    data = data[cols]
    data = drop_na_by_name(data,['Date'])
    data = make_columns_numeric(data,['Qty'])
    data = make_columns_date(data,['Date'])
    return data