# by branch - with details
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric
from etl.utils import make_columns_date


def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,1,3,5,8])
    data.columns = ['desc','date','qty','remark','unit cost']
    data['date'] = data['date'].bfill()
    ids = data[data['desc'].str.contains('Location:', na = False)].index
    data.loc[ids,'Location'] = data.loc[ids,'desc'].str.replace('Location:', '', regex = False)
    data['Location'] = data['Location'].ffill()
    data = make_columns_numeric(data,['qty'],er='coerce')
    data = drop_na_by_name(data,['qty'])
    data = drop_na_by_name(data,['desc'])
    data = make_columns_date(data,['date'])
    data = make_columns_numeric(data,['qty','unit cost'])
    data.columns = ['Product Description','Date', 'Qty', 'Remark','Unit Cost','Location']
    return data