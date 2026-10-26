from __future__ import annotations

from pathlib import Path

import pytest
from application.exporters import export_accounts_json
from application.models import Account


@pytest.mark.integration
def test_export_accounts_pipeline(tmp_path: Path) -> None:
    output = tmp_path / "accounts_export.json"
    accounts = [Account("UA-EXPORT-1", "C-EXPORT", 3200.0)]
    count = export_accounts_json(accounts, output)
    assert count == 1
    assert output.exists()
