from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from pathlib import Path

from application.models import Account


def export_order(order: dict, path: Path | str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(order, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def export_accounts_json(accounts: Iterable[Account], path: Path | str) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(".tmp")
    count = 0

    records = [
        {
            "account_number": a.account_number,
            "client_id": a.client_id,
            "balance": a.balance,
            "status": a.status,
        }
        for a in accounts
    ]

    with temp_path.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
        count = len(records)

    temp_path.replace(output_path)
    return count


def import_accounts_csv(path: Path | str) -> list[Account]:
    input_path = Path(path)
    accounts: list[Account] = []
    with input_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            acc_num = row.get("account_number", "").strip()
            client_id = (row.get("client_id") or row.get("client") or "").strip()
            balance = float(row.get("balance", "0"))
            status = row.get("status", "active").strip().lower() or "active"
            accounts.append(
                Account(account_number=acc_num, client_id=client_id, balance=balance, status=status)
            )  # type: ignore[arg-type]
    return accounts
