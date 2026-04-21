# import xlwings as xw
# import copy

# def get_excel_cols(
#         master_path, 
#         config_list, 
#         data_dict
#     ):

#     def normalize(x):
#         return str(x).strip().lower() if x is not None else ""

#     config_map = {normalize(conf["key"]): conf for conf in config_list}

#     app = xw.App(visible=False, add_book=False)
#     wb = app.books.open(master_path)

#     result = {}

#     try:
#         for job_key in data_dict:
#             norm_job_key = normalize(job_key)

#             if norm_job_key not in config_map:
#                 continue  # skip silently

#             conf = config_map[norm_job_key]
#             new_conf = copy.deepcopy(conf)

#             sheet_name = conf["sheet"]
#             header_row = conf["start_row"] - 1
#             wanted_cols = conf["df_cols"]

#             ws = wb.sheets[sheet_name]
#             last_col = ws.used_range.last_cell.column

#             header_map = {}

#             for col_idx in range(1, last_col + 1):
#                 val = ws.range((header_row, col_idx)).value
#                 norm_val = normalize(val)
#                 if norm_val:
#                     header_map[norm_val] = col_idx

#             excel_cols = [
#                 xw.utils.col_name(header_map[normalize(col)])
#                 for col in wanted_cols
#             ]

#             new_conf["excel_cols"] = excel_cols
#             result[job_key] = new_conf

#     finally:
#         wb.close()
#         app.quit()

#     return result


import xlwings as xw
import copy

def get_excel_cols(
        master_path, 
        config_list, 
        data_dict
    ):

    def normalize(x):
        return str(x).strip().lower() if x is not None else ""

    app = xw.App(visible=False, add_book=False)
    wb = app.books.open(master_path)

    result = {}

    try:
        for conf in config_list:
            new_conf = copy.deepcopy(conf)

            job_key = conf["key"]
            sheet_name = conf["sheet"]
            header_row = conf["start_row"] - 1
            wanted_cols = conf["df_cols"]

            ws = wb.sheets[sheet_name]
            last_col = ws.used_range.last_cell.column

            header_map = {}

            for col_idx in range(1, last_col + 1):
                val = ws.range((header_row, col_idx)).value
                norm_val = normalize(val)
                if norm_val:
                    header_map[norm_val] = col_idx

            excel_cols = [
                xw.utils.col_name(header_map[normalize(col)])
                for col in wanted_cols
            ]

            new_conf["excel_cols"] = excel_cols
            result[job_key] = new_conf

    finally:
        wb.close()
        app.quit()

    return result