from __future__ import annotations

import json
from pathlib import Path

from application.exporters import export_accounts_json, export_order, import_accounts_csv
from application.models import Account


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


def test_export_order_via_tmp_path(tmp_path: Path) -> None:
    output = tmp_path / "order.json"
    order = {"id": 1, "total": 100.0, "status": "paid"}
    export_order(order, output)
    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data == order


def test_csv_import_with_missing_fields(tmp_path: Path) -> None:
    csv_file = tmp_path / "corrupted.csv"
    csv_file.write_text(
        "account_number,client_id,balance\nUA999,,0.0\n",
        encoding="utf-8",
    )
    imported = import_accounts_csv(csv_file)
    assert len(imported) == 1
    assert imported[0].account_number == "UA999"
    assert imported[0].status == "active"


def test_atomic_export_replaces_temp_file(tmp_path: Path) -> None:
    accounts = [Account("UA1", "C1", 50.0)]
    out_file = tmp_path / "target.json"
    export_accounts_json(accounts, out_file)
    assert out_file.exists()
    assert not out_file.with_suffix(".tmp").exists()
