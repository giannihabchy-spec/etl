from pathlib import Path

import pandas as pd


_SHEET_NAME_MAP: dict[str, str] = {
    "summary of sales by customer by item": "summary of sales",
    "purchase master report for all branches": "purchase master report",
    "discount by category by department": "disc by category by dep",
    "discount by description by employee": "disc by desc by employee",
}


def save_cleaned_data(cleaned: dict[str, object], raw_folder: str | Path) -> None:
    """
    Save each DataFrame in `cleaned` to a sheet in an Excel workbook.

    The workbook is named 'Cleaned Data.xlsx' and is created in `raw_folder`,
    which should be the folder containing all the raw data files.

    Sheet names are the dataset names, except for any keys present in
    `_SHEET_NAME_MAP`, in which case the mapped value is used.
    """
    folder_path = Path(raw_folder)
    if not folder_path.exists() or not folder_path.is_dir():
        raise NotADirectoryError(f"Folder not found or not a directory: {folder_path}")

    workbook_path = folder_path / "Cleaned Data.xlsx"

    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        for name, value in cleaned.items():
            if not isinstance(value, pd.DataFrame):
                continue

            sheet_name = _SHEET_NAME_MAP.get(name, name)[:31]

            value.to_excel(writer, sheet_name=sheet_name, index=False)

    return workbook_path

