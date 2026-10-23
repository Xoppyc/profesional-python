from __future__ import annotations

from typing import Any

from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import BankingEntry


def parse_account(
    row: dict[str, str],
    *,
    line_number: int | None = None,
    min_balance: float = 0.0,
    allowed_operations: set[str] | None = None,
) -> BankingEntry:
    allowed_ops = allowed_operations or {"deposit", "withdraw"}

    acc_num = (row.get("account_number") or row.get("account") or "").strip()
    client = (row.get("client") or row.get("name") or "").strip()
    op_raw = (row.get("operation") or "deposit").strip().lower()

    if not acc_num:
        raise RecordValidationError(
            "Missing account number", line_number=line_number, field="account_number"
        )
    if not client:
        raise RecordValidationError("Missing client name", line_number=line_number, field="client")
    if op_raw not in allowed_ops:
        raise RecordValidationError(
            f"Unsupported operation: {op_raw}", line_number=line_number, field="operation"
        )

    try:
        balance = float(row.get("balance", "0"))
    except (ValueError, TypeError) as exc:
        raise RecordValidationError(
            f"Invalid balance: {row.get('balance')}", line_number=line_number, field="balance"
        ) from exc

    try:
        amount = float(row.get("amount", "0"))
    except (ValueError, TypeError) as exc:
        raise RecordValidationError(
            f"Invalid amount: {row.get('amount')}", line_number=line_number, field="amount"
        ) from exc

    if balance < min_balance:
        raise RecordValidationError(
            f"Balance {balance} is below minimum {min_balance}",
            line_number=line_number,
            field="balance",
        )
    if amount <= 0:
        raise RecordValidationError(
            "Amount must be positive", line_number=line_number, field="amount"
        )

    if op_raw == "deposit":
        final_balance = round(balance + amount, 2)
    elif op_raw == "withdraw":
        if balance < amount:
            raise RecordValidationError(
                f"Withdrawal {amount} exceeds balance {balance} (negative balance prohibited)",
                line_number=line_number,
                field="amount",
            )
        final_balance = round(balance - amount, 2)
    else:
        final_balance = balance

    return BankingEntry(
        account_number=acc_num,
        client=client,
        balance=balance,
        operation=op_raw,  # type: ignore[arg-type]
        amount=amount,
        final_balance=final_balance,
    )


def validate_and_compute_entry(row: dict[str, str], config: Any) -> BankingEntry:
    min_bal = getattr(config, "min_balance", 0.0)
    allowed = getattr(config, "allowed_operations", {"deposit", "withdraw"})
    line_no = int(row.get("__line_number__", "0")) or None
    return parse_account(row, line_number=line_no, min_balance=min_bal, allowed_operations=allowed)


parse_student = parse_account
validate_account = parse_account
