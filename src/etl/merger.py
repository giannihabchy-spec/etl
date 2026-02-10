import pandas as pd


def merge(cleaned: dict) -> dict:
    merged = {}

    disc_by_desc = cleaned.get("discount by description by employee")
    sales_by_item = cleaned.get("sales item by transaction")
    disc_by_item = cleaned.get("discount by items")

    if disc_by_desc is not None and sales_by_item is not None:
        disc_by_desc_100 = disc_by_desc[disc_by_desc['Discount_Percentage'] > 0.95].copy()
        merged["disc_by_desc__sales_by_item"] = disc_by_desc_100.merge(
            sales_by_item,
            how = "left",
            on = 'Check',
        )
    
    if disc_by_desc is not None and disc_by_item is not None:
        disc_by_item__disc_by_desc = disc_by_item.merge(
            disc_by_desc,
            how = 'left',
             on = 'Check'
        )
        disc_by_item__disc_by_desc = disc_by_item__disc_by_desc[disc_by_item__disc_by_desc['Discount_Percentage'] > 0.95].copy()
        merged["disc_by_item__disc_by_desc"] = disc_by_item__disc_by_desc

    return merged