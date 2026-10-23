from __future__ import annotations

from pathlib import Path

from stream_processor.analytics import calculate_statistics, calculate_total_balance
from stream_processor.batches import batched_accounts, take_first_n
from stream_processor.filters import (
    filter_by_balance,
    filter_by_client,
    find_by_account_number,
    validate_accounts,
)
from stream_processor.models import AccountRecord
from stream_processor.parsers import parse_csv_rows
from stream_processor.pipeline import build_pipeline
from stream_processor.readers import read_lines
from stream_processor.transformations import apply_operations


def test_stream_reading_and_parsing(tmp_path: Path) -> None:
    csv_file = tmp_path / "accounts.csv"
    csv_file.write_text(
        "account_number,client,balance,operation,amount\n"
        "UA1001,artem kyrychenko,1000.0,deposit,200.0\n"
        "UA1002,olena kovalenko,500.0,withdraw,100.0\n"
        "UA1003,corrupted record,invalid,deposit,-50.0\n",
        encoding="utf-8",
    )

    lines = read_lines(csv_file)
    rows = parse_csv_rows(lines)
    valid_accounts = list(validate_accounts(rows))

    assert len(valid_accounts) == 2
    assert valid_accounts[0].account_number == "UA1001"
    assert valid_accounts[0].amount == 200.0


def test_transformations_prevent_overdraft() -> None:
    accounts = [
        AccountRecord("UA1", "Client A", 100.0, "deposit", 50.0),
        AccountRecord("UA2", "Client B", 200.0, "withdraw", 50.0),
        AccountRecord("UA3", "Client C", 10.0, "withdraw", 100.0),  # overdraft -> rejected
    ]

    processed = list(apply_operations(accounts))
    assert len(processed) == 2
    assert processed[0].balance == 150.0
    assert processed[1].balance == 150.0


def test_filters_and_search() -> None:
    accounts = [
        AccountRecord("UA1", "Artem Kyrychenko", 1500.0, "deposit", 100.0),
        AccountRecord("UA2", "Ivan Franko", 800.0, "deposit", 50.0),
    ]

    by_client = list(filter_by_client(accounts, "artem kyrychenko"))
    assert len(by_client) == 1

    by_balance = list(filter_by_balance(accounts, 1000.0))
    assert len(by_balance) == 1

    found = find_by_account_number(accounts, "UA2")
    assert found is not None
    assert found.client == "Ivan Franko"

    not_found = find_by_account_number(accounts, "NON_EXISTING")
    assert not_found is None


def test_batching_and_first_n() -> None:
    accounts = [
        AccountRecord(f"UA{i}", f"Client {i}", float(i * 100), "deposit", 10.0) for i in range(10)
    ]

    batches = list(batched_accounts(accounts, 3))
    assert len(batches) == 4
    assert len(batches[0]) == 3
    assert len(batches[-1]) == 1

    first_two = list(take_first_n(accounts, 2))
    assert len(first_two) == 2
    assert first_two[0].account_number == "UA0"


def test_analytics_and_statistics() -> None:
    accounts = [
        AccountRecord("UA1", "Client 1", 100.0, "deposit", 10.0),
        AccountRecord("UA2", "Client 2", 200.0, "deposit", 20.0),
        AccountRecord("UA3", "Client 3", 300.0, "deposit", 30.0),
    ]

    total = calculate_total_balance(accounts)
    assert total == 600.0

    stats = calculate_statistics(accounts)
    assert stats["count"] == 3
    assert stats["total"] == 600.0
    assert stats["average"] == 200.0
    assert stats["minimum"] == 100.0
    assert stats["maximum"] == 300.0


def test_full_pipeline_run() -> None:
    data_path = Path("Lab_03/data/input.csv")
    accounts = list(build_pipeline(data_path, minimum_balance=1000.0))
    assert len(accounts) > 0
    for acc in accounts:
        assert acc.balance >= 1000.0
