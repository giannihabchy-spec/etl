JOBS = [
    { # sales by items -> Sales
        "source": "cleaned",
        "key": "sales by items",
        "df_cols": ['Description', 'Qty', 'Total Amount'],
        "sheet": "Sales",
        "excel_cols": ["A","B", "C"],
        "start_row": 2,
    },
]