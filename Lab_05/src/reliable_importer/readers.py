import csv
from collections.abc import Generator
from pathlib import Path


def read_banking_csv(file_path: Path) -> Generator[dict[str, str], None, None]:
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found at: {file_path}")

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader, start=2):
            if not row:
                continue
            row["__line_number__"] = str(row_idx)
            yield row
