import pandas as pd
from etl.utils import make_columns_numeric


def merge(cleaned: dict) -> dict:

    disc_by_desc = cleaned.get("discount by description by employee")
    sales_by_item = cleaned.get("sales item by transaction")
    disc_by_item = cleaned.get("discount by items")
    cols = ['Check', 'Description', 'QTY', 'Discount', 'Amount', 'Discount_Percentage']

    if disc_by_desc is not None and sales_by_item is not None:
        disc_by_desc_100 = disc_by_desc[disc_by_desc['Discount_Percentage'] > 0.95].copy()
        cleaned["disc_by_desc__sales_by_item"] = disc_by_desc_100.merge(
            sales_by_item,
            how = "left",
            on = 'Check',
        )[cols]
    
    if disc_by_desc is not None and disc_by_item is not None:
        disc_by_item__disc_by_desc = disc_by_item.merge(
            disc_by_desc,
            how = 'left',
             on = 'Check'
        )[cols]
        disc_by_item__disc_by_desc = disc_by_item__disc_by_desc[disc_by_item__disc_by_desc['Discount_Percentage'] > 0.95].copy()

        if disc_by_item__disc_by_desc.notna().any().any():

            ids = disc_by_item__disc_by_desc.index
            cleaned['disc_by_item__disc_by_desc'] = make_columns_numeric(disc_by_item__disc_by_desc,['QTY','Discount','Amount','Discount_Percentage'])
            cleaned['discount by items'] = cleaned['discount by items'].drop(index=ids)

    return cleaned