from __future__ import annotations

import argparse
import sys
from pathlib import Path

from etl.config import JOBS
from etl.orchestrator import clean_folder
from etl.merger import merge
from etl.strip_all import strip_all
from etl.special_characters import special_char
from etl.reset_view import reset_workbook_view
from etl.end_to_beg import end_to_beg
from etl.clearer import clear_all
from etl.writer import write_master
import warnings

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style*",
    category=UserWarning,
)


class Spinner:

    def __init__(self, message: str = ""):
        self.message = message
        self.console = Console(force_terminal=True, legacy_windows=True, width=120)
        self._progress: Progress | None = None
        self._task_id: int | None = None

    def __enter__(self):
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        )
        self._progress.start()
        self._task_id = self._progress.add_task(self.message, total=None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._progress:
            self._progress.stop()
        return False


def _step(msg: str) -> None:
    print(msg)
    sys.stdout.flush()


def run_pipeline(base_folder: Path, mode: str = "all") -> None:

    base_folder = base_folder.resolve()

    if not base_folder.is_dir():
        raise NotADirectoryError(f"Folder not found or not a directory: {base_folder}")

    _step(f"▶ Using folder: {base_folder}")

    master_path = base_folder / "Auto Calc.xlsx"
    if not master_path.is_file():
        raise FileNotFoundError(f"Master workbook not found at: {master_path}")

    _step(f"▶ Using master workbook: {master_path.name}")

    with Spinner("   Cleaning..."):
        cleaned = clean_folder(base_folder)
        cleaned = merge(cleaned)
        cleaned = strip_all(cleaned)
        cleaned = special_char(cleaned)

    with Spinner("   Resetting view..."):
        reset_workbook_view(master_path)

    if mode == "all":
        with Spinner("   Ending -> Beg..."):
            end_to_beg(str(master_path))

        with Spinner("   Clearing... "):
            clear_all(str(master_path), JOBS)

        with Spinner("   Writing... "):
            write_master(
                str(master_path),
                cleaned,
                JOBS,
                clear_first=False,
            )
    elif mode == "not-all":
        with Spinner("   Writing... "):
            write_master(
                str(master_path),
                cleaned,
                JOBS,
                clear_first=True,
                suppress_warnings=True,
            )
    else:
        raise ValueError(f"Unsupported mode: {mode!r}")

    _step("✅ ETL pipeline completed.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the ETL pipeline on a folder containing raw Excel files "
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
