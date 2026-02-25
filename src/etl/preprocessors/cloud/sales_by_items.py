import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import drop_na_by_name
from etl.utils import remove_repeated_headers
from etl.utils import make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,2,3])
    data.columns = ['Description','Qty','Total Amount']
    data = drop_na_by_name(data,['Qty'])
    data = remove_repeated_headers(data,'Qty')
    data = make_columns_numeric(data,['Qty','Total Amount'])
    return data