from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import drop_rows
from etl.utils import drop_na_by_name
from etl.utils import remove_repeated_headers
from etl.utils import make_columns_numeric


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,4,6,7])
    data.columns = ['Product Description','Total by item', 'Qty', 'Remark']
    data = drop_rows(data,'Total by item',value='Total by Item:')
    data['Product Description'] = data['Product Description'].ffill()
    data = drop_na_by_name(data,['Qty'])
    data = remove_repeated_headers(data,'Product Description')
    cols = ['Product Description', 'Qty', 'Remark']
    data = data[cols]
    data = make_columns_numeric(data,['Qty'])
    return data