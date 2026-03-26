"""Tests for BudgetCLI data models."""

import pytest

from src.budget.models import Category, Transaction, TransactionType


class TestTransaction:
    """Tests for the Transaction dataclass."""

    def test_create_valid_expense(self) -> None:
        t = Transaction(
            amount=50.0,
            description="Grocery shopping",
            category=Category.FOOD,
            transaction_type=TransactionType.EXPENSE,
        )
        assert t.amount == 50.0
        assert t.description == "Grocery shopping"
        assert t.category == Category.FOOD
        assert t.transaction_type == TransactionType.EXPENSE

    def test_create_valid_income(self) -> None:
        t = Transaction(
            amount=1500.0,
            description="Monthly salary",
            category=Category.SALARY,
            transaction_type=TransactionType.INCOME,
        )
        assert t.transaction_type == TransactionType.INCOME

    def test_default_date_is_today(self) -> None:
        from datetime import date

        t = Transaction(
            amount=10.0,
            description="Coffee",
            category=Category.FOOD,
            transaction_type=TransactionType.EXPENSE,
        )
        assert t.date == date.today()

    def test_custom_date(self) -> None:
        from datetime import date

        custom = date(2025, 1, 15)
        t = Transaction(
            amount=10.0,
            description="Coffee",
            category=Category.FOOD,
            transaction_type=TransactionType.EXPENSE,
            date=custom,
        )
        assert t.date == custom

    def test_raises_if_amount_is_zero(self) -> None:
        with pytest.raises(ValueError, match="Amount must be positive"):
            Transaction(
                amount=0,
                description="Test",
                category=Category.OTHER,
                transaction_type=TransactionType.EXPENSE,
            )

    def test_raises_if_amount_is_negative(self) -> None:
        with pytest.raises(ValueError, match="Amount must be positive"):
            Transaction(
                amount=-10.0,
                description="Test",
                category=Category.OTHER,
                transaction_type=TransactionType.EXPENSE,
            )

    def test_raises_if_description_is_empty(self) -> None:
        with pytest.raises(ValueError, match="Description cannot be empty"):
            Transaction(
                amount=10.0,
                description="   ",
                category=Category.OTHER,
                transaction_type=TransactionType.EXPENSE,
            )


class TestTransactionType:
    """Tests for the TransactionType enum."""

    def test_income_value(self) -> None:
        assert TransactionType.INCOME.value == "income"

    def test_expense_value(self) -> None:
        assert TransactionType.EXPENSE.value == "expense"


class TestCategory:
    """Tests for the Category enum."""

    def test_all_categories_exist(self) -> None:
        expected = {
            "FOOD",
            "TRANSPORT",
            "ENTERTAINMENT",
            "HEALTH",
            "UTILITIES",
            "SALARY",
            "OTHER",
        }
        assert {c.name for c in Category} == expected
