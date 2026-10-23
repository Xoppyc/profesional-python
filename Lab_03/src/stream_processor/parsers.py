from __future__ import annotations

import csv
from collections.abc import Iterable, Iterator


def parse_csv_rows(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    # Consume line streams progressively to avoid materializing intermediate sequences
    reader = csv.DictReader(lines)
    yield from reader
