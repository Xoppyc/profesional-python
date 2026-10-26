from __future__ import annotations

from sqlalchemy.orm import Session

from bank_storage.models import TransactionModel
from bank_storage.repositories import AccountRepository


class InsufficientBalanceError(Exception):
    pass


class NegativeAmountError(ValueError):
    pass


def deposit_money(session: Session, account_number: str, amount: float) -> float:
    if amount <= 0:
        raise NegativeAmountError("Deposit amount must be strictly positive")

    repo = AccountRepository(session)
    account = repo.get_by_number(account_number)
    if not account:
        raise ValueError(f"Account {account_number} not found")

    try:
        account.balance += amount
        tx = TransactionModel(account_id=account.id, operation="deposit", amount=amount)
        session.add(tx)
        session.commit()
        session.refresh(account)
        return account.balance
    except Exception:
        session.rollback()
        raise


def withdraw_money(session: Session, account_number: str, amount: float) -> float:
    if amount <= 0:
        raise NegativeAmountError("Withdrawal amount must be strictly positive")

    repo = AccountRepository(session)
    account = repo.get_by_number(account_number)
    if not account:
        raise ValueError(f"Account {account_number} not found")

    if account.balance < amount:
        raise InsufficientBalanceError(f"Insufficient balance on account {account_number}")

    try:
        account.balance -= amount
        tx = TransactionModel(account_id=account.id, operation="withdraw", amount=amount)
        session.add(tx)
        session.commit()
        session.refresh(account)
        return account.balance
    except Exception:
        session.rollback()
        raise


def transfer_money(
    session: Session, source_num: str, target_num: str, amount: float
) -> tuple[float, float]:
    if amount <= 0:
        raise NegativeAmountError("Transfer amount must be positive")

    repo = AccountRepository(session)
    source = repo.get_by_number(source_num)
    target = repo.get_by_number(target_num)

    if not source or not target:
        raise ValueError("Source or target account not found")

    if source.balance < amount:
        raise InsufficientBalanceError(f"Insufficient balance on account {source_num}")

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


def calculate_total_funds(session: Session) -> float:
    repo = AccountRepository(session)
    return repo.total_funds()
