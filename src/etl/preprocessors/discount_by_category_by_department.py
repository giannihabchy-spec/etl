import pandas as pd
from etl.utils import read 
from etl.utils import keep_cols_by_index
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric

def preprocess(path):

    data = read(path)

    data = keep_cols_by_index(data,[1,4])

    data.columns=['Category','Total']

    data = drop_na_by_name(data,['Category'])

    data = make_columns_numeric(data,['Total'])

    return data