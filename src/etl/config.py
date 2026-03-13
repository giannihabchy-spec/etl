JOBS_CLOUD = [

    { #  -> programming summary sales -> SP ####----------
    "key": "programming summary sales",
    "df_cols": ['Description', 'Price','Category', 'Group'],
    "sheet": "SP",
    "excel_cols": ['A','B','C','D'],
    "start_row": 2,
    },

    { # sales by items -> Sales #### ----------
        "key": "sales by items",
        "df_cols": ['Description', 'Qty', 'Total Amount'],
        "sheet": "Sales",
        "excel_cols": ["A","B", "C"],
        "start_row": 2,
    },

    { # discount by category by department -> Disc. Cat. #### ----------
    "key": "discount by category by department",
    "df_cols": ['Category', 'Total'],
    "sheet": "Disc. Cat.",
    "excel_cols": ["A","B"],
    "start_row": 2,
    },

    { # disc_by_desc__sales_by_item -> Discount #### ----------
    "key": "disc_by_desc__disc_by_invoice",
    "df_cols": ['Description', 'QTY'],
    "sheet": "Discount",
    "excel_cols": ["A","B"],
    "start_row": 2,
    },

    { # discount by items -> Discount
    "key": "discount by items",
    "df_cols": ['Description', 'QTY'],
    "sheet": "Discount",
    "excel_cols": ["A","B"],
    "start_row": 2,
    },

    { # purchase master report for all branches -> Purchase #### ----------
    "key": "purchase master report for all branches",
    "df_cols": ['Location', 'Product Description','Qty','Total','Supplier','Invoice','Purchase Date'],
    "sheet": "Purchase",
    "excel_cols": ["A","C","D","I","J","K","L"],
    "start_row": 2,
    },

    { # inventory production -> PRD #### ----------
    "key": "inventory production",
    "df_cols": ['Location Description','Product Description','Qty'],
    "sheet": "PRD",
    "excel_cols": ['A','B','C'],
    "start_row": 2,
    },

    { # summary of sales by customer by item -> W.Inv #### ----------
    "key": "summary of sales by customer by item",
    "df_cols": ['Location','Qty','Description','Remark','Date','Total Price','Invoice','Customer'],
    "sheet": "W.Inv",
    "excel_cols": ['A','C','E','F','K','L','M','N'],
    "start_row": 2,
    },

    { # wastage report
    "key": "wastage report",
    "df_cols": ['Location','Qty','Product Description','Remark','Date'],
    "sheet": "W.Inv",
    "excel_cols": ['A','C','E','F','K'],
    "start_row": 2,
    },

    { # sales item wastage -> W.Sal #### ----------
    "key": "sales item wastage",
    "df_cols": ['Product Description', 'Qty', 'Remark','Date','Unit Cost'],
    "sheet": "W.Sal",
    "excel_cols": ['A','B','F','I','J'],
    "start_row": 2,
    },

    { # inventory history -> Ending #### ----------
    "key": "inventory history",
    "df_cols": ['Location','Product Description', 'Qty'],
    "sheet": "Ending",
    "excel_cols": ['A','B','C'],
    "start_row": 2,
    },

    { # programming summary inventory -> Unit Cost #### ----------
    "key": "programming summary inventory",
    "df_cols": ['Category','Group','Product Description','Qty I F','Unit','Pur Unit','Qty Pur','Inv Unit','Avg Cost'],
    "sheet": "Unit Cost",
    "excel_cols": ['A','B','C','D','E','F','G','H','I'],
    "start_row": 2,
    },

    { # requisition summary -> IN OUT ####----------
    "key": "requisition summary",
    "df_cols": ['Product','From Location','From Branch','To Location','To Branch','Qty','Date'],
    "sheet": "IN OUT",
    "excel_cols": ['A','B','C','D','E','F','J'],
    "start_row": 2,
    },

    { # requisition summary IB
    "key": "requisition summary IB",
    "df_cols": ['Product','From Location','From Branch','To Location','To Branch','Qty','Date'],
    "sheet": "IN OUT",
    "excel_cols": ['A','B','C','D','E','F','J'],
    "start_row": 2,
    },

    { # sales items ingredients -> Recipes ####----------
    "key": "sales items ingredients",
    "df_cols": ['Item','Ingredient','Qty'],
    "sheet": "Recipes",
    "excel_cols": ['C','D','E'],
    "start_row": 2,
    }

]

# ----------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------

JOBS_LOCAL = [

    { #  -> list sales items -> SP ####----------
    "key": "list sales items",
    "df_cols": ['Description', 'Price','Category', 'Group'],
    "sheet": "SP",
    "excel_cols": ['A','B','C','D'],
    "start_row": 2,
    },

    { # sales by menu by items -> Sales #### ----------
        "key": "sales by menu by items",
        "df_cols": ['Description', 'Qty', 'Total Amount'],
        "sheet": "Sales",
        "excel_cols": ["A","B", "C"],
        "start_row": 2,
    },

    { # discount by category -> Disc. Cat. #### ----------
    "key": "discount by category",
    "df_cols": ['Category', 'Total'],
    "sheet": "Disc. Cat.",
    "excel_cols": ["A","B"],
    "start_row": 2,
    },

    { # disc_by_desc__sales_by_item -> Discount #### ----------
    "key": "disc_by_desc__disc_by_invoice",
    "df_cols": ['Description', 'QTY'],
    "sheet": "Discount",
    "excel_cols": ["A","B"],
    "start_row": 2,
    },

    { # discount by items -> Discount
    "key": "discount by items",
    "df_cols": ['Description', 'QTY'],
    "sheet": "Discount",
    "excel_cols": ["A","B"],
    "start_row": 2,
    },

    { # purchase with all details -> Purchase #### ----------
    "key": "purchase with all details",
    "df_cols": ['Location', 'Product Description','Qty','Total','Supplier','Invoice','Purchase Date'],
    "sheet": "Purchase",
    "excel_cols": ["A","C","D","I","J","K","L"],
    "start_row": 2,
    },

    { # inventory production -> PRD #### ----------
    "key": "inventory production",
    "df_cols": ['Location Description','Product Description','Qty'],
    "sheet": "PRD",
    "excel_cols": ['A','B','C'],
    "start_row": 2,
    },

    { # inventory / summary of sales by customer by items -> W.Inv #### ----------
    "key": "inventory / summary of sales by customer by items",
    "df_cols": ['Location','Qty','Description','Remark','Date','Total Price','Invoice','Customer'],
    "sheet": "W.Inv",
    "excel_cols": ['A','C','E','F','K','L','M','N'],
    "start_row": 2,
    },

    { # inventory wastage items
    "key": "inventory wastage items",
    "df_cols": ['Location','Qty','Product Description','Remark','Date'],
    "sheet": "W.Inv",
    "excel_cols": ['A','C','E','F','K'],
    "start_row": 2,
    },

    { # sales / summary of sales by customer by items -> W.Sal #### ----------
    "key": "sales / summary of sales by customer by items",
    "df_cols": ['Description', 'Qty', 'Remark','Date','Total Price','Invoice','Customer'],
    "sheet": "W.Sal",
    "excel_cols": ['A','B','F','I','K','L','M'],
    "start_row": 2,
    },

    { # sales wastage items
    "key": "sales wastage items",
    "df_cols": ['Product Description', 'Qty', 'Remark','Date','Unit Cost'],
    "sheet": "W.Sal",
    "excel_cols": ['A','B','F','I','J'],
    "start_row": 2,
    },

    { # inventory history -> Ending #### ----------
    "key": "inventory history",
    "df_cols": ['Location','Product Description', 'Qty'],
    "sheet": "Ending",
    "excel_cols": ['A','B','C'],
    "start_row": 2,
    },

    { # programming summary inventory -> Unit Cost #### ----------
    "key": "programming summary inventory",
    "df_cols": ['Category','Group','Product Description','Qty I F','Unit','Pur Unit','Qty Pur','Inv Unit','Avg Cost'],
    "sheet": "Unit Cost",
    "excel_cols": ['A','B','C','D','E','F','G','H','I'],
    "start_row": 2,
    },

    { # requisition summary -> IN OUT ####----------
    "key": "requisition summary",
    "df_cols": ['Product','From Location','From Branch','To Location','To Branch','Qty','Date'],
    "sheet": "IN OUT",
    "excel_cols": ['A','B','C','D','E','F','J'],
    "start_row": 2,
    },

    { # sales items ingredients -> Recipes ####----------
    "key": "sales items ingredients",
    "df_cols": ['Item','Ingredient','Qty'],
    "sheet": "Recipes",
    "excel_cols": ['C','D','E'],
    "start_row": 2,
    }


]


def get_jobs(source: str) -> list[dict]:
    if source == "cloud":
        return JOBS_CLOUD
    if source == "local":
        return JOBS_LOCAL
    raise ValueError(f"Unknown source: {source!r}. Use 'cloud' or 'local'.")