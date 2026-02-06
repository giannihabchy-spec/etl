import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import remove_repeated_headers
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,3,5])
    data.columns = ['Product Description', 'Qty', 'Remark']
    data = remove_repeated_headers(data,'Qty')
    data = drop_na_by_name(data,['Product Description'])
    data = make_columns_numeric(data,['Qty'],er='coerce')
    data = drop_na_by_name(data,['Qty'])
    return data