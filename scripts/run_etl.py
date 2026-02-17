from __future__ import annotations

import argparse
import sys
import threading
import time
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


class Spinner:
    """Green dots moving in a square pattern."""
    
    GREEN = "\033[92m"
    RESET = "\033[0m"
    
    PATTERNS = [
        "● · · ·",  
        "· ● · ·",  
        "· · ● ·",  
        "· · · ●",  
    ]
    
    def __init__(self, message: str = ""):
        self.message = message
        self.pattern_idx = 0
        self.running = False
        self.thread = None
    
    def _spin(self):
        while self.running:
            pattern = self.PATTERNS[self.pattern_idx % len(self.PATTERNS)]
            green_pattern = pattern.replace("●", f"{self.GREEN}●{self.RESET}")
            sys.stdout.write(f"\r{self.message} {green_pattern}")
            sys.stdout.flush()
            self.pattern_idx += 1
            time.sleep(0.2)
    
    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.3)
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()


def _step(msg: str) -> None:
    """Print a simple, flush-immediate step message."""
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

    _step("① Cleaning raw files...")
    cleaned = clean_folder(base_folder)

    _step("② Merging derived datasets...")
    cleaned = merge(cleaned)

    if mode == "all":
        _step("③ Copying 'Ending' sheet to 'Beg'...")
        with Spinner("   Ending -> Beg"):
            end_to_beg(str(master_path))

        _step("④ Clearing...")
        with Spinner("   Clearing "):
            clear_all(str(master_path), JOBS)

        _step("⑤ Writing...")
        with Spinner("   Writing "):
            write_master(
                str(master_path),
                cleaned,
                JOBS,
                clear_first=False,
            )
    elif mode == "not-all":
        _step("③ Writing...")
        with Spinner("   Writing "):
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
