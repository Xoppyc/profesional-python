from __future__ import annotations

from pathlib import Path

import pytest
from application.exporters import import_accounts_csv


@pytest.mark.integration
def test_csv_import_pipeline(tmp_path: Path) -> None:
    csv_file = tmp_path / "accounts.csv"
    csv_file.write_text(
        "account_number,client_id,balance,status\nUA101,C1,1500.0,active\nUA102,C2,2500.5,active\n",
        encoding="utf-8",
    )

    imported_accounts = import_accounts_csv(csv_file)
    assert len(imported_accounts) == 2
    assert imported_accounts[0].account_number == "UA101"
