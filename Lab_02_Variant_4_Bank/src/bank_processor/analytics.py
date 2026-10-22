from collections import defaultdict

from bank_processor.models import AccountRecord, AccountType


def build_account_index(
    accounts: list[AccountRecord],
) -> dict[str, AccountRecord]:
    # Pre-index by account_number for O(1) key lookups instead of O(N) iterative scans
    return {acc.account_number: acc for acc in accounts}


def find_account_by_number(
    index: dict[str, AccountRecord],
    account_number: str,
) -> AccountRecord | None:
    return index.get(account_number)


def group_by_account_type(
    accounts: list[AccountRecord],
) -> dict[AccountType, list[AccountRecord]]:
    grouped: dict[AccountType, list[AccountRecord]] = defaultdict(list)
    for acc in accounts:
        grouped[acc.account_type].append(acc)
    return dict(grouped)


def calculate_total_funds(
    accounts: list[AccountRecord],
) -> float:
    return sum(acc.balance for acc in accounts)


def calculate_average_balance(
    accounts: list[AccountRecord],
) -> float:
    if not accounts:
        return 0.0
    return calculate_total_funds(accounts) / len(accounts)


def find_highest_balance_account(
    accounts: list[AccountRecord],
) -> AccountRecord | None:
    if not accounts:
        return None
    return max(accounts, key=lambda acc: acc.balance)


def filter_by_min_balance(
    accounts: list[AccountRecord],
    min_balance: float,
) -> list[AccountRecord]:
    return [acc for acc in accounts if acc.balance >= min_balance]


def sort_accounts_by_balance(
    accounts: list[AccountRecord],
    descending: bool = True,
) -> list[AccountRecord]:
    return sorted(accounts, key=lambda acc: acc.balance, reverse=descending)
