import pytest
from bank_catalog.models import AccountEntity


@pytest.mark.parametrize(
    "initial,deposit_amt,expected",
    [
        (100.0, 50.0, 150.0),
        (0.0, 1000.0, 1000.0),
        (500.0, 250.75, 750.75),
    ],
)
def test_parametrized_deposits(initial: float, deposit_amt: float, expected: float) -> None:
    acc = AccountEntity("UA1", "C1", initial)
    acc.deposit(deposit_amt)
    assert acc.balance == expected


def test_withdraw_limits() -> None:
    acc = AccountEntity("UA2", "C1", 200.0)
    with pytest.raises(ValueError, match="Insufficient balance"):
        acc.withdraw(250.0)

    acc.status = "blocked"
    with pytest.raises(PermissionError, match="inactive"):
        acc.deposit(100.0)
