from __future__ import annotations

import csv
from collections.abc import Iterator
from pathlib import Path

from reliable_importer.exceptions import DataImportError


def read_csv_rows(path: Path | str) -> Iterator[tuple[int, dict[str, str]]]:
    file_path = Path(path)
    if not file_path.exists():
        raise DataImportError(f"Input file not found at: {file_path}")

    try:
        with file_path.open(mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for line_number, row in enumerate(reader, start=2):
                if not row or all(not v.strip() for v in row.values() if isinstance(v, str)):
                    continue
                yield line_number, row
    except (UnicodeDecodeError, OSError) as exc:
        raise DataImportError(f"Failed to read CSV stream: {exc}") from exc


def read_banking_csv(file_path: Path | str) -> Iterator[dict[str, str]]:
    for line_number, row in read_csv_rows(file_path):
        row["__line_number__"] = str(line_number)
        yield row
