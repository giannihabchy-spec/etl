# Put Rate Manually

import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import drop_na_by_name
from etl.utils import remove_repeated_headers
from etl.utils import make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[1,2,3,4,5,7,10])
    data.columns = ['Product Description','Buying U','Qty B. F.','Stock U','Qty ','Usage U','AV. Cost']
    data = drop_na_by_name(data,['Stock U'])
    data = remove_repeated_headers(data,'Product Description')
    data = make_columns_numeric(data,['Qty B. F.','Qty ','AV. Cost'])
    return data