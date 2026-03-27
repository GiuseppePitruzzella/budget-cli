"""Report generation functions for BudgetCLI."""

from dataclasses import dataclass
from datetime import date

from src.budget.models import Category, Transaction, TransactionType


@dataclass
class Summary:
    """Aggregate summary of a list of transactions."""

    total_income: float
    total_expenses: float
    balance: float
    transaction_count: int


def generate_summary(transactions: list[Transaction]) -> Summary:
    """Return aggregated totals for a list of transactions."""
    income = sum(
        t.amount for t in transactions if t.transaction_type == TransactionType.INCOME
    )
    expenses = sum(
        t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE
    )
    return Summary(
        total_income=income,
        total_expenses=expenses,
        balance=income - expenses,
        transaction_count=len(transactions),
    )


def breakdown_by_category(transactions: list[Transaction]) -> dict[Category, float]:
    """Return the total amount spent/received per category."""
    result: dict[Category, float] = {}
    for t in transactions:
        result[t.category] = result.get(t.category, 0.0) + t.amount
    return result


def filter_by_date_range(
    transactions: list[Transaction],
    start: date,
    end: date,
) -> list[Transaction]:
    """Return transactions whose date falls within [start, end] inclusive."""
    return [t for t in transactions if start <= t.date <= end]
