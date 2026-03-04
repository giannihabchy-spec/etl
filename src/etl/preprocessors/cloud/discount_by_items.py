import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric

def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,3,4])
    data.columns = ['Check','Description','QTY']
    data = drop_na_by_name(data,['Description','QTY'])
    data = make_columns_numeric(data,['QTY'], er='coerce')
    data = drop_na_by_name(data,['QTY'])
    data = data.reset_index(drop = True)
    return data