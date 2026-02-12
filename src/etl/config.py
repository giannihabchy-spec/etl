JOBS = [

    { #  -> programming summary sales -> SP ####----------
    "key": "programming summary sales",
    "df_cols": ['Description', 'Price Level 1'],
    "sheet": "SP",
    "excel_cols": ['A','B'],
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
    "key": "disc_by_desc__sales_by_item",
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
    "excel_cols": ["A","c","d","I","J","K","L"],
    "start_row": 2,
    },

    { # inventory production -> PRD #### ----------
    "key": "inventory production",
    "df_cols": ['Location Description','Product Description','Qty'],
    "sheet": "PRD",
    "excel_cols": ['A','B','C'],
    "start_row": 2,
    },

    { # wastage report -> W.Inv #### ----------
    "key": "wastage report",
    "df_cols": ['Location','Qty','Product Description','Remark'],
    "sheet": "W.Inv",
    "excel_cols": ['A','C','E','F'],
    "start_row": 2,
    },

    { # summary of sales by customer by item -> W.Inv 
    "key": "summary of sales by customer by item",
    "df_cols": ['Location','Qty','Description'],
    "sheet": "W.Inv",
    "excel_cols": ['A','C','E'],
    "start_row": 2,
    },

    { # sales item wastage -> W.Sal #### ----------
    "key": "sales item wastage",
    "df_cols": ['Product Description', 'Qty', 'Remark'],
    "sheet": "W.Sal",
    "excel_cols": ['A','B','F'],
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
    "sheet": "Ending",
    "excel_cols": ['A','B','C','D','E','F','G','H','I'],
    "start_row": 2,
    },

    { #  -> requisition summary -> IN OUT ####----------
    "key": "requisition summary",
    "df_cols": ['Product','From Location','From Branch','To Location','To Branch','Qty','Date'],
    "sheet": "IN OUT",
    "excel_cols": ['A','B','C','D','E','F','J'],
    "start_row": 2,
    },

    { #  -> requisition summary IB
    "key": "requisition summary IB",
    "df_cols": ['Product','From Location','From Branch','To Location','To Branch','Qty','Date'],
    "sheet": "IN OUT",
    "excel_cols": ['A','B','C','D','E','F','J'],
    "start_row": 2,
    }

]