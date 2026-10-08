from bank_manager.models import Account
from bank_manager.services import (
    calculate_total_balance,
    create_account,
    deposit,
    filter_by_min_balance,
    find_largest_account,
    withdraw,
)


def run_demo() -> None:
    accounts: list[Account] = []

    acc1 = create_account(accounts, "UA10001", "Artem Kyrychenko", 1500.0)
    acc2 = create_account(accounts, "UA10002", "Olena Kovalenko", 3200.0)
    acc3 = create_account(accounts, "UA10003", "Ivan Petrenko", 750.0)

    print(f"Created accounts: {len(accounts)}")
    deposit(accounts, "UA10001", 500.0)
    print(f"UA10001 after deposit 500: {acc1.balance}")

    withdraw(accounts, "UA10002", 200.0)
    print(f"UA10002 after withdraw 200: {acc2.balance}")

    total = calculate_total_balance(accounts)
    print(f"Total bank funds: {total}")

    largest = find_largest_account(accounts)
    if largest:
        print(f"Largest account: {largest.account_number} ({largest.client_name}) - {largest.balance}")

    high_net_worth = filter_by_min_balance(accounts, 2000.0)
    print(f"Accounts with balance >= 2000: {[a.account_number for a in high_net_worth]}")


if __name__ == "__main__":
    run_demo()
