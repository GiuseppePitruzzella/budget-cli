"""Tests for the Ledger business logic."""

from datetime import date

import pytest

from src.budget.ledger import Ledger
from src.budget.models import Category, Transaction, TransactionType


def make_transaction(
    amount: float = 10.0,
    description: str = "Test",
    category: Category = Category.OTHER,
    transaction_type: TransactionType = TransactionType.EXPENSE,
) -> Transaction:
    return Transaction(
        amount=amount,
        description=description,
        category=category,
        transaction_type=transaction_type,
        date=date(2025, 11, 1),
    )


class TestLedgerAdd:
    def test_add_increases_count(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction())
        assert len(ledger.all()) == 1

    def test_add_preserves_transaction(self) -> None:
        ledger = Ledger()
        t = make_transaction(amount=99.0, description="Specific")
        ledger.add(t)
        assert ledger.all()[0] == t

    def test_add_multiple_transactions(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction())
        ledger.add(make_transaction())
        assert len(ledger.all()) == 2


class TestLedgerRemove:
    def test_remove_returns_correct_transaction(self) -> None:
        ledger = Ledger()
        t = make_transaction(description="Target")
        ledger.add(t)
        removed = ledger.remove(0)
        assert removed == t

    def test_remove_decreases_count(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction())
        ledger.remove(0)
        assert len(ledger.all()) == 0

    def test_remove_raises_on_invalid_index(self) -> None:
        ledger = Ledger()
        with pytest.raises(IndexError):
            ledger.remove(0)

    def test_remove_raises_on_negative_index(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction())
        with pytest.raises(IndexError):
            ledger.remove(-1)


class TestLedgerAll:
    def test_all_returns_empty_list_by_default(self) -> None:
        assert not Ledger().all()

    def test_all_returns_copy(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction())
        copy = ledger.all()
        copy.clear()
        assert len(ledger.all()) == 1


class TestLedgerFilterByCategory:
    def test_filter_returns_matching_transactions(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction(category=Category.FOOD))
        ledger.add(make_transaction(category=Category.TRANSPORT))
        result = ledger.filter_by_category(Category.FOOD)
        assert len(result) == 1
        assert result[0].category == Category.FOOD

    def test_filter_returns_empty_when_no_match(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction(category=Category.FOOD))
        assert ledger.filter_by_category(Category.HEALTH) == []


class TestLedgerFilterByType:
    def test_filter_by_income(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction(transaction_type=TransactionType.INCOME))
        ledger.add(make_transaction(transaction_type=TransactionType.EXPENSE))
        result = ledger.filter_by_type(TransactionType.INCOME)
        assert len(result) == 1

    def test_filter_by_expense(self) -> None:
        ledger = Ledger()
        ledger.add(make_transaction(transaction_type=TransactionType.EXPENSE))
        ledger.add(make_transaction(transaction_type=TransactionType.INCOME))
        result = ledger.filter_by_type(TransactionType.EXPENSE)
        assert len(result) == 1


class TestLedgerBalance:
    def test_balance_is_zero_for_empty_ledger(self) -> None:
        assert Ledger().balance() == 0.0

    def test_balance_with_only_income(self) -> None:
        ledger = Ledger()
        ledger.add(
            make_transaction(amount=500.0, transaction_type=TransactionType.INCOME)
        )
        assert ledger.balance() == 500.0

    def test_balance_with_only_expenses(self) -> None:
        ledger = Ledger()
        ledger.add(
            make_transaction(amount=200.0, transaction_type=TransactionType.EXPENSE)
        )
        assert ledger.balance() == -200.0

    def test_balance_with_mixed_transactions(self) -> None:
        ledger = Ledger()
        ledger.add(
            make_transaction(amount=1000.0, transaction_type=TransactionType.INCOME)
        )
        ledger.add(
            make_transaction(amount=300.0, transaction_type=TransactionType.EXPENSE)
        )
        assert ledger.balance() == 700.0

    def test_balance_with_initial_transactions(self) -> None:
        transactions = [
            make_transaction(amount=50.0, transaction_type=TransactionType.INCOME)
        ]
        ledger = Ledger(transactions=transactions)
        assert ledger.balance() == 50.0
