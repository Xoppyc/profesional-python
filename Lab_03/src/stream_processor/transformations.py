from __future__ import annotations

from collections.abc import Iterable, Iterator

from stream_processor.models import AccountRecord


def apply_operations(accounts: Iterable[AccountRecord]) -> Iterator[AccountRecord]:
    # Enforce non-negative ledger balance to maintain double-entry integrity
    for acc in accounts:
        if acc.operation == "deposit":
            new_balance = round(acc.balance + acc.amount, 2)
            yield acc._replace(balance=new_balance)
        elif acc.operation == "withdraw":
            if acc.balance >= acc.amount:
                new_balance = round(acc.balance - acc.amount, 2)
                yield acc._replace(balance=new_balance)
            else:
                # Omit transactions that would cause ledger overdraft
                continue
        else:
            yield acc


def normalize_names(accounts: Iterable[AccountRecord]) -> Iterator[AccountRecord]:
    for acc in accounts:
        yield acc._replace(client=acc.client.strip().title())


normalize_client_names = normalize_names
process_transactions = apply_operations
