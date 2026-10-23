from __future__ import annotations

from pathlib import Path

from reliable_importer.exporters import export_accounts_json
from reliable_importer.services import ImportStatistics, filter_by_balance, import_accounts


def test_import_accounts_streaming(tmp_path: Path) -> None:
    csv_file = tmp_path / "accounts.csv"
    csv_file.write_text(
        "account_number,client,balance,operation,amount\n"
        "UA1001,Artem Kyrychenko,1000.0,deposit,200.0\n"
        "UA1002,Olena Kovalenko,500.0,withdraw,100.0\n"
        "UA1003,Corrupted,invalid,deposit,50.0\n",
        encoding="utf-8",
    )

    stats = ImportStatistics()
    accounts = list(import_accounts(csv_file, skip_invalid=True, statistics=stats))

    assert len(accounts) == 2
    assert stats.total == 3
    assert stats.valid == 2
    assert stats.invalid == 1


def test_filter_and_export_accounts(tmp_path: Path) -> None:
    csv_file = tmp_path / "accounts.csv"
    csv_file.write_text(
        "account_number,client,balance,operation,amount\n"
        "UA1001,Artem,1000.0,deposit,200.0\n"
        "UA1002,Olena,200.0,deposit,100.0\n",
        encoding="utf-8",
    )

    accounts = import_accounts(csv_file)
    filtered = filter_by_balance(accounts, minimum_balance=500.0)

    out_file = tmp_path / "out.json"
    exported = export_accounts_json(filtered, out_file)

    assert exported == 1
    assert out_file.exists()
