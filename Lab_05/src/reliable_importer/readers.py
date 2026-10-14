import csv
from pathlib import Path
from typing import Generator
from reliable_importer.exceptions import InvalidRecordError
from reliable_importer.models import BankingEntry


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
