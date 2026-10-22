from sqlalchemy.orm import Session

from bank_storage.models import TransactionModel
from bank_storage.repositories import AccountRepository


class InsufficientBalanceError(Exception):
    pass


def transfer_money(
    session: Session, source_num: str, target_num: str, amount: float
) -> tuple[float, float]:
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    repo = AccountRepository(session)
    source = repo.get_by_number(source_num)
    target = repo.get_by_number(target_num)

    if not source or not target:
        raise ValueError("Source or target account not found")

    if source.balance < amount:
        raise InsufficientBalanceError(f"Insufficient balance on account {source_num}")

    # Use explicit transaction block to guarantee atomic balance deduction and transaction ledger creation
    try:
        source.balance -= amount
        target.balance += amount

        tx_out = TransactionModel(account_id=source.id, operation="transfer_out", amount=amount)
        tx_in = TransactionModel(account_id=target.id, operation="transfer_in", amount=amount)

        session.add(tx_out)
        session.add(tx_in)
        session.commit()
        return source.balance, target.balance
    except Exception:
        session.rollback()
        raise
