from reliable_importer.config import ImporterConfig
from reliable_importer.exceptions import InvalidRecordError
from reliable_importer.logging_config import mask_sensitive_account
from reliable_importer.models import BankingEntry


def validate_and_compute_entry(row: dict[str, str], config: ImporterConfig) -> BankingEntry:
    acc_num = row.get("account_number", "").strip()
    client = row.get("client", "").strip()
    operation = row.get("operation", "").strip().lower()

    if not acc_num or not client:
        raise InvalidRecordError("Missing required account number or client name")

    if operation not in config.allowed_operations:
        raise InvalidRecordError(f"Unsupported operation: {operation}")

    try:
        balance = float(row.get("balance", "0"))
        amount = float(row.get("amount", "0"))
    except ValueError:
        raise InvalidRecordError("Non-numeric balance or amount value")

    if amount <= 0:
        raise InvalidRecordError("Transaction amount must be strictly positive")

    if balance < config.min_balance:
        raise InvalidRecordError(f"Balance cannot start below minimum {config.min_balance}")

    if operation == "deposit":
        final_balance = balance + amount
    elif operation == "withdraw":
        if balance < amount:
            raise InvalidRecordError(f"Withdrawal of {amount} would produce negative balance")
        final_balance = balance - amount
    else:
        raise InvalidRecordError("Unknown operation")

    return BankingEntry(
        account_number=acc_num,
        client=client,
        balance=balance,
        operation=operation,  # type: ignore[arg-type]
        amount=amount,
        final_balance=final_balance,
    )
