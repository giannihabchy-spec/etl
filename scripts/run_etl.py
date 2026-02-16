from __future__ import annotations
import argparse
from pathlib import Path
from etl.config import JOBS
from etl.orchestrator import clean_folder
from etl.merger import merge
from etl.end_to_beg import end_to_beg
from etl.clearer import clear_all
from etl.writer import write_master
import warnings

warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style*",
    category=UserWarning,
)



def run_pipeline(base_folder: Path, mode: str = "all") -> None:
    """
    Run the ETL pipeline.

    Parameters
    ----------
    base_folder:
        Folder containing all raw report files and the master workbook
        named 'Auto Calc.xlsx'.
    mode:
        'all' (default) or 'not-all'.
    """
    base_folder = base_folder.resolve()

    if not base_folder.is_dir():
        raise NotADirectoryError(f"Folder not found or not a directory: {base_folder}")

    master_path = base_folder / "Auto Calc.xlsx"
    if not master_path.is_file():
        raise FileNotFoundError(f"Master workbook not found at: {master_path}")

    # 1) Clean raw files in the given folder
    cleaned = clean_folder(base_folder)

    # 2) Merge derived datasets
    cleaned = merge(cleaned)

    if mode == "all":
        # 3) Copy Ending -> Beg in master workbook
        end_to_beg(str(master_path))

        # 4) Clear all configured ranges
        clear_all(str(master_path), JOBS)

        # 5) Write, appending if data already exists (clear_first disabled)
        write_master(
            str(master_path),
            cleaned,
            JOBS,
            clear_first=False,
        )
    elif mode == "not-all":
        # Run without end_to_beg / clear_all, but clear_first enabled
        write_master(
            str(master_path),
            cleaned,
            JOBS,
            clear_first=True,
            suppress_warnings=True,
        )
    else:
        raise ValueError(f"Unsupported mode: {mode!r}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the EKC ETL pipeline on a folder containing raw Excel files "
            "and a master workbook named 'Auto Calc.xlsx'."
        )
    )

    parser.add_argument(
        "folder",
        type=str,
        help="Path to folder with raw files and 'Auto Calc.xlsx'.",
    )

    parser.add_argument(
        "--mode",
        choices=["all", "not-all"],
        default="all",
        help=(
            "Run mode. 'all' (default) runs clean_folder, merge, end_to_beg, "
            "clear_all, then write_master with clear_first disabled. "
            "'not-all' runs clean_folder, merge, then write_master with "
            "clear_first enabled."
        ),
    )

    args = parser.parse_args()

    run_pipeline(Path(args.folder), mode=args.mode)


if __name__ == "__main__":
    main()
