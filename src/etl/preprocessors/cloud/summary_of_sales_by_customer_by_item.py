import pandas as pd
from etl.utils import read
from etl.utils import keep_cols_by_index
from etl.utils import remove_repeated_headers
from etl.utils import drop_na_by_name
from etl.utils import make_columns_numeric
from etl.utils import clean_check

def preprocess(path):
    data = read(path)
    data = keep_cols_by_index(data,[0,1,2,7])
    data.columns = ['Product Code', 'Description', 'Qty', 'Total Price']
    id = data[data['Product Code'] == 'Product Code'].index[0] # Keep only the rows after the first Header
    data = data.iloc[id:].copy()
    data = remove_repeated_headers(data,'Product Code')

    # Create 'Customer' from 'Product Code'
    cust_ids = data[data['Product Code'].str.contains('Customer Name: ',na=False)].index
    data.loc[cust_ids,'Customer'] = data.loc[cust_ids,'Product Code'].str.replace('Customer Name: ','',regex = False)
    data['Customer'] = data['Customer'].ffill()

    # Create 'Location' from 'Product Code'
    loc_ids = data[data['Product Code'].str.contains('Location: ',na=False)].index
    data.loc[loc_ids,'Location'] = data.loc[loc_ids,'Product Code'].str.replace('Location: ','',regex = False)
    data['Location'] = data['Location'].ffill()

    # 'Date' is 'Product Code' converted to type date
    data['Date'] = pd.to_datetime(data['Product Code'],errors='coerce').dt.date
    data['Date'] = data['Date'].ffill()

    # Create 'Invoice' from 'Product Code'
    inv_ids = data[data['Product Code'].str.contains('Invoice Number: ', na = False)].index
    data.loc[inv_ids,'Invoice'] = data.loc[inv_ids,'Product Code'].str.replace('Invoice Number: ', '', regex = False)
    data['Invoice'] = data['Invoice'].ffill()
    data = clean_check(data,['Invoice'])

    data = drop_na_by_name(data,['Description'])
    data = data.drop(columns='Product Code').copy()
    data = drop_na_by_name(data,['Qty'])
    data = make_columns_numeric(data,['Qty','Total Price'])
    return data