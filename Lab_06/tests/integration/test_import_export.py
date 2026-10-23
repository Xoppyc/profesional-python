from __future__ import annotations

from pathlib import Path

from application.exporters import export_accounts_json, import_accounts_csv


def test_csv_import_and_json_export_integration(tmp_path: Path) -> None:
    csv_file = tmp_path / "accounts.csv"
    csv_file.write_text(
        "account_number,client_id,balance,status\nUA101,C1,1500.0,active\nUA102,C2,2500.5,active\n",
        encoding="utf-8",
    )

    imported_accounts = import_accounts_csv(csv_file)
    assert len(imported_accounts) == 2
    assert imported_accounts[0].account_number == "UA101"
    assert imported_accounts[0].balance == 1500.0

    json_file = tmp_path / "accounts.json"
    exported_count = export_accounts_json(imported_accounts, json_file)

    assert exported_count == 2
    assert json_file.exists()
    assert "UA101" in json_file.read_text(encoding="utf-8")
