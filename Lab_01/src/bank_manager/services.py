from bank_manager.models import Account


def create_account(
    accounts: list[Account],
    account_number: str,
    client_name: str,
    initial_balance: float = 0.0,
) -> Account:
    if find_by_account_number(accounts, account_number) is not None:
        raise ValueError(f"Account with number {account_number} already exists")

    account = Account(
        account_number=account_number,
        client_name=client_name,
        balance=initial_balance,
    )
    accounts.append(account)
    return account


def deposit(
    accounts: list[Account],
    account_number: str,
    amount: float,
) -> Account:
    if amount <= 0:
        raise ValueError("Deposit amount must be strictly positive")

    account = find_by_account_number(accounts, account_number)
    if account is None:
        raise ValueError(f"Account {account_number} not found")

    account.balance += amount
    return account


def withdraw(
    accounts: list[Account],
    account_number: str,
    amount: float,
) -> Account:
    if amount <= 0:
        raise ValueError("Withdrawal amount must be strictly positive")

    account = find_by_account_number(accounts, account_number)
    if account is None:
        raise ValueError(f"Account {account_number} not found")

    if account.balance < amount:
        # Disallow negative balances in accordance with bank account invariant
        raise ValueError("Insufficient funds for withdrawal")

    account.balance -= amount
    return account


def get_balance(
    accounts: list[Account],
    account_number: str,
) -> float:
    account = find_by_account_number(accounts, account_number)
    if account is None:
        raise ValueError(f"Account {account_number} not found")
    return account.balance


def find_by_account_number(
    accounts: list[Account],
    account_number: str,
) -> Account | None:
    for account in accounts:
        if account.account_number == account_number:
            return account
    return None


def calculate_total_balance(
    accounts: list[Account],
) -> float:
    return sum(account.balance for account in accounts)


def filter_by_min_balance(
    accounts: list[Account],
    min_balance: float,
) -> list[Account]:
    return [account for account in accounts if account.balance >= min_balance]


def find_largest_account(
    accounts: list[Account],
) -> Account | None:
    if not accounts:
        return None
    return max(accounts, key=lambda acc: acc.balance)
