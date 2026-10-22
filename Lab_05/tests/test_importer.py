from pathlib import Path

import pytest
from reliable_importer.config import ImporterConfig
from reliable_importer.exceptions import InvalidRecordError
from reliable_importer.exporters import export_entries_atomically
from reliable_importer.validators import validate_and_compute_entry


@pytest.fixture
def test_config(tmp_path: Path) -> ImporterConfig:
    return ImporterConfig(
        strict_mode=False,
        min_balance=0.0,
        max_single_transfer=500000.0,
        allowed_operations={"deposit", "withdraw"},
        input_csv=tmp_path / "in.csv",
        output_json=tmp_path / "out.json",
        log_file=tmp_path / "log.txt",
    )


def test_validate_entry_success(test_config: ImporterConfig) -> None:
    row = {
        "account_number": "UA5001",
        "client": "Artem Kyrychenko",
        "balance": "1000.0",
        "operation": "deposit",
        "amount": "500.0",
    }
    entry = validate_and_compute_entry(row, test_config)
    assert entry.final_balance == 1500.0


def test_withdraw_overdraft_rejected(test_config: ImporterConfig) -> None:
    row = {
        "account_number": "UA5002",
        "client": "Olena",
        "balance": "300.0",
        "operation": "withdraw",
        "amount": "500.0",
    }
    with pytest.raises(InvalidRecordError, match="negative balance"):
        validate_and_compute_entry(row, test_config)


def test_atomic_export(tmp_path: Path, test_config: ImporterConfig) -> None:
    row = {
        "account_number": "UA1",
        "client": "Test",
        "balance": "100.0",
        "operation": "deposit",
        "amount": "50.0",
    }
    entry = validate_and_compute_entry(row, test_config)
    out_file = tmp_path / "export.json"
    export_entries_atomically([entry], out_file)

    assert out_file.exists()
    assert not out_file.with_suffix(".tmp").exists()
