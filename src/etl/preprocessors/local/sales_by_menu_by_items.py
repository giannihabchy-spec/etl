from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,3])
    data.columns = ['Description', 'Qty']
    data = drop_na_by_name(data,['Qty'])
    ids = data[data['Description'].isna()].index
    data.loc[ids,'Total Amount'] = data.loc[ids,'Qty']
    data['Total Amount'] = data['Total Amount'].shift(-1)
    data = drop_na_by_name(data,['Description'])
    data = make_columns_numeric(data,['Qty','Total Amount'])
    return data