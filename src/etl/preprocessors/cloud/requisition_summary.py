# by Details

import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import remove_repeated_headers
from etl.utils import drop_na_by_name
from etl.utils import make_columns_date, make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,1,2,3,4,6,])
    data.columns = ['From Branch', 'To Branch', 'To Location', 'Date', 'Product', 'Qty']
    data = remove_repeated_headers(data,'Product')

    # Creating 'From Location'
    ids = data[data['From Branch'].str.contains('From Location: ', na = False)].index
    data.loc[ids,'From Location'] = data.loc[ids,'From Branch'].str.replace('From Location: ', '', regex = False)
    data['From Location'] = data['From Location'].ffill()
    data = drop_na_by_name(data,['Product'])

    cols = ['Product','From Location','From Branch','To Location','To Branch','Qty','Date']
    data = data[cols]
    data = make_columns_numeric(data,['Qty'])
    data = make_columns_date(data,['Date'])
    return data