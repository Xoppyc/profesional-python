from __future__ import annotations

from domain_app.models import CurrentAccount, Customer, SavingsAccount
from domain_app.repositories import AccountRepository
from domain_app.services import BankingService


class ConsoleNotifier:
    def notify(self, message: str) -> None:
        print(f"[NOTIFICATION] {message}")

    def send(self, message: str) -> None:
        self.notify(message)


def main() -> None:
    repo = AccountRepository()
    notifier = ConsoleNotifier()
    service = BankingService(repo=repo, notifier=notifier)

    alice = Customer("CUST1", "Artem Kyrychenko", "artem@example.com")
    bob = Customer("CUST2", "Olena Kovalenko", "olena@example.com")

    acc1 = SavingsAccount("UA1001", alice, initial_balance=5000.0)
    acc2 = CurrentAccount("UA1002", bob, initial_balance=2000.0)

    repo.add(acc1)
    repo.add(acc2)

    print("Initial total funds:", service.calculate_total_funds())
    service.transfer("UA1001", "UA1002", 500.0)
    print("Post-transfer total funds:", service.calculate_total_funds())


if __name__ == "__main__":
    main()
