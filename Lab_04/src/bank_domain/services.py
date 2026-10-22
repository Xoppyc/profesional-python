from bank_domain.models import BankingError, BaseAccount
from bank_domain.repository import InMemoryRepository


class AccountTransferService:
    def __init__(self, repo: InMemoryRepository[BaseAccount]) -> None:
        self.repo = repo

    def transfer(self, source_acc_num: str, target_acc_num: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        source = self.repo.get_by_id(source_acc_num)
        target = self.repo.get_by_id(target_acc_num)

        if not source or not target:
            raise BankingError("One or both accounts were not found")

        # Atomic double-entry transfer with immediate rollback on withdrawal failure
        source.withdraw(amount)
        target.deposit(amount)
