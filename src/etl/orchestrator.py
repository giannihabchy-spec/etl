from pathlib import Path
import re
from typing import Literal

import pandas as pd

from etl.preprocessors.cloud import discount_by_category_by_department
from etl.preprocessors.cloud import discount_by_description_by_employee
from etl.preprocessors.cloud import discount_by_items
from etl.preprocessors.cloud import inventory_history
from etl.preprocessors.cloud import inventory_production
from etl.preprocessors.cloud import programming_summary_inventory
from etl.preprocessors.cloud import programming_summary_sales
from etl.preprocessors.cloud import purchase_master_report_for_all_branches
from etl.preprocessors.cloud import requisition_summary
from etl.preprocessors.cloud import requisition_summary_IB
from etl.preprocessors.cloud import sales_by_items
from etl.preprocessors.cloud import sales_item_by_transaction
from etl.preprocessors.cloud import sales_item_wastage
from etl.preprocessors.cloud import sales_items_ingerdients
from etl.preprocessors.cloud import summary_of_sales_by_customer_by_item
from etl.preprocessors.cloud import wastage_report

from etl.preprocessors.local import list_sales_items
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local
# from etl.preprocessors.local




cleaner_by_code = {
    'cloud' : {
        "REP_I_0022.xlsx": ("sales items ingredients", sales_items_ingerdients.preprocess),
        "REP_I_00023D_rows.xlsx": ("wastage report", wastage_report.preprocess),
        "REP_I_0024.xlsx": ("inventory production", inventory_production.preprocess),
        "REP_I_0033_rows.xlsx": ("inventory history", inventory_history.preprocess),
        "REP_I_0044.xlsx": ("programming summary inventory", programming_summary_inventory.preprocess),
        "REP_I_00074.xlsx": ("sales item wastage", sales_item_wastage.preprocess),
        "REP_I_0087.xlsx": ("requisition summary", requisition_summary.preprocess),
        "REP_I_0087_IB.xlsx": ("requisition summary IB",requisition_summary_IB.preprocess),
        "REP_I_00268.xlsx": ("summary of sales by customer by item",summary_of_sales_by_customer_by_item.preprocess),
        "REP_I_00462.xlsx": ("purchase master report for all branches",purchase_master_report_for_all_branches.preprocess),
        "rep_s_00016.xlsx": ("discount by items", discount_by_items.preprocess),
        "rep_s_00161.xlsx": ("discount by category by department",discount_by_category_by_department.preprocess),
        "REP_S_00175.xlsx": ("sales item by transaction", sales_item_by_transaction.preprocess),
        "REP_S_00178.xlsx": ("programming summary sales", programming_summary_sales.preprocess),
        "rep_s_00191_rows.xlsx": ("sales by items", sales_by_items.preprocess),
        "rep_s_00438.xlsx": ("discount by description by employee",discount_by_description_by_employee.preprocess),

    },

    'local' : {
        'rep_s_00188.xls': ('list sales items', list_sales_items.preprocess)
    }
}


def _is_requisition_summary_ib_filename(filename: str) -> bool:
    """Match REP_I_0087_IB.xlsx and variants like REP_I_0087_IB (1).xlsx."""
    return re.fullmatch(r"REP_I_0087_IB(?: \(\d+\))?\.xlsx", filename) is not None


def clean_folder(folder: str | Path, source: Literal["cloud", "local"] = "cloud", log_func=print) -> dict[str, object]:
    folder = Path(folder)
    if not folder.exists() or not folder.is_dir():
        raise NotADirectoryError(f"Folder not found or not a directory: {folder}")
    if source not in cleaner_by_code:
        raise ValueError(f"source must be 'cloud' or 'local', got {source!r}")

    cleaners = cleaner_by_code[source]
    cleaned: dict[str, object] = {}
    ib_files = [
        p
        for p in folder.iterdir()
        if p.is_file() and _is_requisition_summary_ib_filename(p.name)
    ]
    multi_ib = len(ib_files) > 1

    for p in folder.iterdir():
        if not p.is_file():
            continue

        if multi_ib and _is_requisition_summary_ib_filename(p.name):
            ib_index = (
                sum(1 for k in cleaned.keys() if k.startswith("requisition summary IB "))
                + 1
            )
            output_name = f"requisition summary IB {ib_index}"
            cleaner = requisition_summary_IB.preprocess

            try:
                result = cleaner(str(p))
                cleaned[output_name] = result

                if isinstance(result, pd.DataFrame):
                    nan_cols = result.columns[result.isna().any()].tolist()
                    if nan_cols:
                        log_func(f"⚠ NaNs in {output_name}: {nan_cols}")

                log_func(f"Cleaned {p.name} -> {output_name}")

            except Exception as e:
                log_func(f"Failed cleaning {p.name} -> {output_name}\n{e}")

            continue

        entry = cleaners.get(p.name)
        if entry is None:
            continue

        output_name, cleaner = entry

        try:
            result = cleaner(str(p))
            cleaned[output_name] = result

            if isinstance(result, pd.DataFrame):
                nan_cols = result.columns[result.isna().any()].tolist()
                if nan_cols:
                    log_func(f"⚠ NaNs in {output_name}: {nan_cols}")

            log_func(f"Cleaned {p.name} -> {output_name}")

        except Exception as e:
            log_func(f"Failed cleaning {p.name} -> {output_name}\n{e}")

    return cleaned
