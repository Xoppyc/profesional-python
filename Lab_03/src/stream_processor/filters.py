from __future__ import annotations

from collections.abc import Iterable, Iterator

from stream_processor.models import AccountRecord


def validate_accounts(rows: Iterable[dict[str, str]]) -> Iterator[AccountRecord]:
    # Filter malformed or negative ledger amounts at ingestion boundary
    for row in rows:
        try:
            account_number = (
                row.get("account_number") or row.get("account") or row.get("id") or ""
            ).strip()
            client = (row.get("client") or row.get("client_name") or row.get("name") or "").strip()
            balance = float(row.get("balance", "0"))
            operation = (row.get("operation") or "deposit").strip().lower()
            amount = float(row.get("amount", "0"))
        except (ValueError, TypeError):
            continue

        if not account_number or not client:
            continue
        if balance < 0 or amount <= 0:
            continue
        if operation not in {"deposit", "withdraw", "transfer"}:
            continue

        yield AccountRecord(
            account_number=account_number,
            client=client,
            balance=balance,
            operation=operation,
            amount=amount,
        )


def filter_by_client(
    accounts: Iterable[AccountRecord],
    client_name: str,
) -> Iterator[AccountRecord]:
    target = client_name.strip().lower()
    for account in accounts:
        if account.client.strip().lower() == target:
            yield account


def filter_by_balance(
    accounts: Iterable[AccountRecord],
    minimum_balance: float,
) -> Iterator[AccountRecord]:
    for account in accounts:
        if account.balance >= minimum_balance:
            yield account


def find_by_account_number(
    accounts: Iterable[AccountRecord],
    account_number: str,
) -> AccountRecord | None:
    # Terminate early upon finding matching identity to avoid consuming tail items
    target = account_number.strip().upper()
    for account in accounts:
        if account.account_number.strip().upper() == target:
            return account
    return None


# Backward and semantic aliases
validate_records = validate_accounts
filter_by_min_balance = filter_by_balance
search_by_account_number = find_by_account_number
find_account = find_by_account_number
