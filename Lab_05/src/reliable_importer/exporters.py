from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from reliable_importer.exceptions import DataExportError
from reliable_importer.models import BankingEntry


def export_accounts_json(
    accounts: Iterable[BankingEntry],
    path: Path | str,
) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    count = 0

    try:
        with temp_path.open("w", encoding="utf-8") as file:
            file.write("[\n")
            first = True
            for account in accounts:
                if not first:
                    file.write(",\n")
                entry_dict = account.to_dict() if hasattr(account, "to_dict") else dict(account)
                file.write("  " + json.dumps(entry_dict, ensure_ascii=False))
                first = False
                count += 1
            file.write("\n]\n")

        # Atomic replacement to protect against partially flushed disk writes
        temp_path.replace(output_path)
        return count
    except Exception as exc:
        if temp_path.exists():
            temp_path.unlink()
        raise DataExportError(f"Failed to export accounts to {output_path}: {exc}") from exc


def export_entries_atomically(entries: list[BankingEntry], output_path: Path | str) -> None:
    export_accounts_json(entries, output_path)


export_students_json = export_accounts_json
export_json = export_accounts_json
