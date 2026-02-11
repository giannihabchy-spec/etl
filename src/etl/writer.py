import pandas as pd
import xlwings as xw

def write_master(
    master_path: str,
    cleaned: dict[str, pd.DataFrame],
    jobs: list[dict],
    output_path: str | None = None,
    clear_first: bool = False,
) -> None:
    
    if output_path is None:
        output_path = master_path

    app = xw.App(visible=False, add_book=False)
    try:
        wb = app.books.open(master_path)
        src = cleaned

        for job in jobs:
            try:
                df = src[job["key"]][job["df_cols"]].copy()
                sht = wb.sheets[job["sheet"]]
            except KeyError as e:
                print(f"⚠ {job.get('key','?')} not available: {e}")
                continue

            if clear_first:
                start_row = job["start_row"]
                for col in job["excel_cols"]:
                    last_used = sht.range(f"{col}{sht.cells.last_cell.row}").end("up").row
                    end_row = max(last_used, start_row)
                    sht.range(f"{col}{start_row}:{col}{end_row}").value = None

            start_cell = f"{job['excel_cols'][0]}{job['start_row']}"
            sht.range(start_cell).options(index=False, header=False).value = df.to_numpy()

        wb.save(output_path)
        wb.close()
    finally:
        app.quit()

