from bank_processor.analytics import (
    build_account_index,
    calculate_average_balance,
    calculate_total_funds,
    find_account_by_number,
    find_highest_balance_account,
    group_by_account_type,
    sort_accounts_by_balance,
)
from bank_processor.decorators import measure_execution_time
from bank_processor.models import AccountRecord


@measure_execution_time
def run_analytics_suite() -> None:
    dataset: list[AccountRecord] = [
        AccountRecord("UA2001", "Artem Kyrychenko", 45000.0, "checking"),
        AccountRecord("UA2002", "Maksym Polishchuk", 120000.0, "deposit"),
        AccountRecord("UA2003", "Yulia Bondar", 8500.0, "savings"),
        AccountRecord("UA2004", "Dmytro Moroz", 24000.0, "checking"),
        AccountRecord("UA2005", "Svitlana Tkachenko", 68000.0, "deposit"),
        AccountRecord("UA2006", "Oleg Shevchenko", 150000.0, "business"),
    ]

    index = build_account_index(dataset)
    acc = find_account_by_number(index, "UA2002")
    print(f"Indexed lookup UA2002: {acc}")

    total = calculate_total_funds(dataset)
    avg = calculate_average_balance(dataset)
    highest = find_highest_balance_account(dataset)

    print(f"Total: {total:.2f} UAH | Average: {avg:.2f} UAH")
    if highest:
        print(f"Top Account: {highest.account_number} ({highest.balance} UAH)")

    grouped = group_by_account_type(dataset)
    print("Grouped by account type:")
    for acc_type, group in grouped.items():
        print(f"  - {acc_type}: {len(group)} accounts")

    sorted_accs = sort_accounts_by_balance(dataset)
    print(f"Rank 1: {sorted_accs[0].account_number} ({sorted_accs[0].balance} UAH)")


if __name__ == "__main__":
    run_analytics_suite()
