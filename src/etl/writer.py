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

        for job in jobs:
            try:
                df = cleaned[job["key"]].loc[:, job["df_cols"]].copy()
                sht = wb.sheets[job["sheet"]]
            except KeyError as e:
                print(f"⚠ {job.get('key','?')} not available: {e}")
                continue

            start_row = int(job["start_row"])
            first_col = job["excel_cols"][0]
            last_col = job["excel_cols"][-1]

            # target block: from start_row down to bottom of sheet
            block = sht.range(
                f"{first_col}{start_row}:{last_col}{sht.cells.last_cell.row}"
            )

            if clear_first:
                block.value = None
                write_row = start_row
            else:
                vals = block.value  # 2D list or None
                if not vals:
                    write_row = start_row
                else:
                    # find last row in the block that has ANY non-empty cell
                    last_nonempty_offset = -1
                    for i, row in enumerate(vals):
                        if row is None:
                            continue
                        if any(cell not in (None, "") for cell in row):
                            last_nonempty_offset = i

                    write_row = start_row if last_nonempty_offset == -1 else start_row + last_nonempty_offset + 1

            start_cell = f"{first_col}{write_row}"
            sht.range(start_cell).options(index=False, header=False).value = df.to_numpy()

        wb.save(output_path)
        wb.close()
    finally:
        app.quit()
