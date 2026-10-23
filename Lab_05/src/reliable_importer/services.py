from __future__ import annotations

import logging
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import BankingEntry
from reliable_importer.readers import read_csv_rows
from reliable_importer.validators import parse_account

logger = logging.getLogger(__name__)


@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0


def import_accounts(
    path: Path | str,
    *,
    skip_invalid: bool = True,
    statistics: ImportStatistics | None = None,
    min_balance: float = 0.0,
    allowed_operations: set[str] | None = None,
) -> Iterator[BankingEntry]:
    stats = statistics if statistics is not None else ImportStatistics()

    for line_number, row in read_csv_rows(path):
        stats.total += 1
        try:
            entry = parse_account(
                row,
                line_number=line_number,
                min_balance=min_balance,
                allowed_operations=allowed_operations,
            )
        except RecordValidationError as error:
            stats.invalid += 1
            # Redact confidential data: do not log balances or raw amounts
            logger.warning(
                "Invalid record at line %s in field '%s': %s",
                error.line_number,
                error.field,
                error,
            )
            if skip_invalid:
                continue
            raise

        stats.valid += 1
        yield entry


def filter_by_balance(
    accounts: Iterable[BankingEntry],
    minimum_balance: float,
) -> Iterator[BankingEntry]:
    for account in accounts:
        if account.balance >= minimum_balance:
            yield account


import_students = import_accounts
filter_by_grade = filter_by_balance
