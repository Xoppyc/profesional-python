import pytest
from bank_stream.models import StreamTransaction
from bank_stream.pipeline import (
    batch_stream,
    filter_by_balance_threshold,
    filter_by_client_stream,
    find_first_matching,
    parse_csv_stream,
    stream_total_balance,
    take_first_n,
    validate_transaction_stream,
)


@pytest.fixture
def sample_csv_lines() -> list[str]:
    return [
        "transaction_id,account_number,client_name,operation,amount,current_balance",
        "TX1,UA1001,Artem Kyrychenko,deposit,500.0,2500.0",
        "TX2,UA1002,Olena Kovalenko,withdraw,100.0,400.0",
        "TX3,UA1003,Corrupted Line,-50.0,-10.0",  # invalid
        "TX4,UA1001,Artem Kyrychenko,withdraw,200.0,2300.0",
        "TX5,UA1005,Ivan Franko,deposit,1000.0,7800.0",
    ]


def test_parse_and_validate(sample_csv_lines: list[str]) -> None:
    raw_stream = parse_csv_stream(sample_csv_lines)
    valid_stream = list(validate_transaction_stream(raw_stream))
    # 4 valid items expected, corrupted one rejected
    assert len(valid_stream) == 4


def test_client_filter_and_take(sample_csv_lines: list[str]) -> None:
    valid_stream = validate_transaction_stream(parse_csv_stream(sample_csv_lines))
    artem_txs = list(filter_by_client_stream(valid_stream, "Artem Kyrychenko"))
    assert len(artem_txs) == 2
    first_one = list(take_first_n(artem_txs, 1))
    assert len(first_one) == 1
    assert first_one[0].transaction_id == "TX1"


def test_stream_aggregations(sample_csv_lines: list[str]) -> None:
    valid_stream = list(validate_transaction_stream(parse_csv_stream(sample_csv_lines)))
    total = stream_total_balance(valid_stream)
    assert total == 2500.0 + 400.0 + 2300.0 + 7800.0


def test_batching() -> None:
    items = list(range(10))
    batches = list(batch_stream(items, 3))
    assert batches == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
