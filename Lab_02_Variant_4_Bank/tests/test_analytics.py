import pytest
from bank_processor.models import AccountRecord
from bank_processor.analytics import (
    build_account_index,
    calculate_average_balance,
    calculate_total_funds,
    filter_by_min_balance,
    find_account_by_number,
    find_highest_balance_account,
    group_by_account_type,
    sort_accounts_by_balance,
)


@pytest.fixture
def sample_records() -> list[AccountRecord]:
    return [
        AccountRecord("UA1", "Alice", 1000.0, "checking"),
        AccountRecord("UA2", "Bob", 3000.0, "savings"),
        AccountRecord("UA3", "Charlie", 5000.0, "checking"),
    ]


def test_index_lookup(sample_records: list[AccountRecord]) -> None:
    index = build_account_index(sample_records)
    assert len(index) == 3
    assert find_account_by_number(index, "UA2") == sample_records[1]
    assert find_account_by_number(index, "NONEXISTENT") is None


def test_grouping(sample_records: list[AccountRecord]) -> None:
    grouped = group_by_account_type(sample_records)
    assert len(grouped["checking"]) == 2
    assert len(grouped["savings"]) == 1


def test_calculations(sample_records: list[AccountRecord]) -> None:
    assert calculate_total_funds(sample_records) == 9000.0
    assert calculate_average_balance(sample_records) == 3000.0
    highest = find_highest_balance_account(sample_records)
    assert highest is not None and highest.account_number == "UA3"


def test_sort_and_filter(sample_records: list[AccountRecord]) -> None:
    filtered = filter_by_min_balance(sample_records, 2500.0)
    assert len(filtered) == 2
    sorted_accs = sort_accounts_by_balance(sample_records, descending=True)
    assert sorted_accs[0].balance == 5000.0
