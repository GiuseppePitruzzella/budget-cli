"""Tests for report generation functions."""

from datetime import date

from src.budget.models import Category, Transaction, TransactionType
from src.budget.reports import (
    breakdown_by_category,
    filter_by_date_range,
    generate_summary,
)


def make_transaction(
    amount: float = 10.0,
    category: Category = Category.OTHER,
    transaction_type: TransactionType = TransactionType.EXPENSE,
    tx_date: date = date(2025, 11, 1),
) -> Transaction:
    return Transaction(
        amount=amount,
        description="Test",
        category=category,
        transaction_type=transaction_type,
        date=tx_date,
    )


class TestGenerateSummary:
    def test_empty_list_returns_zeros(self) -> None:
        s = generate_summary([])
        assert s.total_income == 0.0
        assert s.total_expenses == 0.0
        assert s.balance == 0.0
        assert s.transaction_count == 0

    def test_only_income(self) -> None:
        s = generate_summary(
            [make_transaction(amount=500.0, transaction_type=TransactionType.INCOME)]
        )
        assert s.total_income == 500.0
        assert s.total_expenses == 0.0
        assert s.balance == 500.0

    def test_only_expenses(self) -> None:
        s = generate_summary(
            [make_transaction(amount=200.0, transaction_type=TransactionType.EXPENSE)]
        )
        assert s.total_income == 0.0
        assert s.total_expenses == 200.0
        assert s.balance == -200.0

    def test_mixed_transactions(self) -> None:
        transactions = [
            make_transaction(amount=1000.0, transaction_type=TransactionType.INCOME),
            make_transaction(amount=300.0, transaction_type=TransactionType.EXPENSE),
            make_transaction(amount=150.0, transaction_type=TransactionType.EXPENSE),
        ]
        s = generate_summary(transactions)
        assert s.total_income == 1000.0
        assert s.total_expenses == 450.0
        assert s.balance == 550.0
        assert s.transaction_count == 3

    def test_transaction_count(self) -> None:
        transactions = [make_transaction() for _ in range(5)]
        assert generate_summary(transactions).transaction_count == 5


class TestBreakdownByCategory:
    def test_single_category(self) -> None:
        t = make_transaction(amount=30.0, category=Category.FOOD)
        result = breakdown_by_category([t])
        assert result[Category.FOOD] == 30.0

    def test_multiple_categories(self) -> None:
        transactions = [
            make_transaction(amount=20.0, category=Category.FOOD),
            make_transaction(amount=15.0, category=Category.TRANSPORT),
        ]
        result = breakdown_by_category(transactions)
        assert result[Category.FOOD] == 20.0
        assert result[Category.TRANSPORT] == 15.0

    def test_same_category_is_summed(self) -> None:
        transactions = [
            make_transaction(amount=10.0, category=Category.FOOD),
            make_transaction(amount=25.0, category=Category.FOOD),
        ]
        result = breakdown_by_category(transactions)
        assert result[Category.FOOD] == 35.0

    def test_empty_list_returns_empty_dict(self) -> None:
        assert breakdown_by_category([]) == {}


class TestFilterByDateRange:
    def test_returns_transactions_within_range(self) -> None:
        t = make_transaction(tx_date=date(2025, 11, 15))
        result = filter_by_date_range([t], date(2025, 11, 1), date(2025, 11, 30))
        assert len(result) == 1

    def test_start_boundary_is_inclusive(self) -> None:
        t = make_transaction(tx_date=date(2025, 11, 1))
        result = filter_by_date_range([t], date(2025, 11, 1), date(2025, 11, 30))
        assert len(result) == 1

    def test_end_boundary_is_inclusive(self) -> None:
        t = make_transaction(tx_date=date(2025, 11, 30))
        result = filter_by_date_range([t], date(2025, 11, 1), date(2025, 11, 30))
        assert len(result) == 1

    def test_excludes_transactions_outside_range(self) -> None:
        t = make_transaction(tx_date=date(2025, 10, 1))
        result = filter_by_date_range([t], date(2025, 11, 1), date(2025, 11, 30))
        assert result == []

    def test_empty_list_returns_empty(self) -> None:
        result = filter_by_date_range([], date(2025, 11, 1), date(2025, 11, 30))
        assert result == []
