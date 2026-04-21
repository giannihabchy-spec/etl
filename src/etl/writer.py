import pandas as pd
import xlwings as xw

def write_master(
    master_path: str,
    cleaned: dict[str, pd.DataFrame],
    jobs: list[dict],
    output_path: str | None = None,
    suppress_warnings: bool = False,
    log_func=print
) -> None:
    if output_path is None:
        output_path = master_path

    app = xw.App(visible=False, add_book=False)
    try:
        wb = app.books.open(master_path)

        for job in jobs:
            try:
                df = cleaned[job["key"]].copy()
                sht = wb.sheets[job["sheet"]]
            except KeyError:
                if not suppress_warnings:
                    log_func(f"⚠ {job.get('key','?')} not available")
                continue

            log_func(f"{job.get('key')} -> {job.get('sheet')}")

            cols = list(job["cols"])
            start_row = int(job["start_row"])
            header_row = start_row - 1

            # case-insensitive df column mapping
            df_col_map = {str(c).strip().lower(): c for c in df.columns}

            # read excel headers from header row
            last_col = sht.used_range.last_cell.column
            header_values = sht.range((header_row, 1), (header_row, last_col)).value
            if header_values is None:
                header_values = []
            elif not isinstance(header_values, list):
                header_values = [header_values]

            # case-insensitive excel header mapping -> column index
            excel_col_map = {
                str(v).strip().lower(): i
                for i, v in enumerate(header_values, start=1)
                if v not in (None, "")
            }

            # keep same behavior: select requested columns first
            df_real_cols = [df_col_map[col.strip().lower()] for col in cols]
            df = df.loc[:, df_real_cols]

            # find where to append based on matching excel headers
            last_row = start_row - 1
            bottom = sht.cells.last_cell.row

            for col in cols:
                excel_col_idx = excel_col_map[col.strip().lower()]
                vals = sht.range((start_row, excel_col_idx), (bottom, excel_col_idx)).value

                if vals is None:
                    continue
                if not isinstance(vals, list):
                    vals = [vals]

                for i, v in enumerate(vals):
                    if v not in (None, ""):
                        last_row = max(last_row, start_row + i)

            write_row = start_row if last_row < start_row else last_row + 1

            # write each column to the matching excel header column
            for requested_col, real_df_col in zip(cols, df_real_cols):
                excel_col_idx = excel_col_map[requested_col.strip().lower()]
                sht.range((write_row, excel_col_idx)).options(index=False, header=False).value = df[[real_df_col]].to_numpy()

        wb.save(output_path)
        wb.close()
    finally:
        app.quit()