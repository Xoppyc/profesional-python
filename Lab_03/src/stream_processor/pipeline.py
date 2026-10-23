from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from stream_processor.filters import filter_by_balance, validate_accounts
from stream_processor.models import AccountRecord
from stream_processor.parsers import parse_csv_rows
from stream_processor.readers import read_lines
from stream_processor.transformations import apply_operations, normalize_names


def build_pipeline(
    path: Path | str,
    minimum_balance: float = 0.0,
) -> Iterator[AccountRecord]:
    # Compose lazy generator stages into an end-to-end processing pipeline
    lines = read_lines(path)
    rows = parse_csv_rows(lines)
    validated = validate_accounts(rows)
    normalized = normalize_names(validated)
    processed = apply_operations(normalized)
    return filter_by_balance(processed, minimum_balance)
