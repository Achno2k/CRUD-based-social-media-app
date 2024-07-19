import pytest

def func (num : int):
    return num + 1

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise Exception("Insufficient Funds")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def amt_bank_account():
    return BankAccount(50)


# the naming of the functions does matter, every test function must be prefixxed with test
@pytest.mark.parametrize("num, expected", [
    (2, 3),
    (4, 5),
    (1, 2)
])
def test_func(num: int, expected: int):
    assert func(num) == expected 

def test_default_bank_account(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_amt_bank_account(amt_bank_account):
    assert amt_bank_account.balance == 50


def test_exception(amt_bank_account):
    with pytest.raises(Exception):
        amt_bank_account.withdraw(60)