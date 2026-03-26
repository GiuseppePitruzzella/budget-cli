"""Data models for BudgetCLI transactions."""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class TransactionType(Enum):
    """Type of a financial transaction."""

    INCOME = "income"
    EXPENSE = "expense"


class Category(Enum):
    """Category of a financial transaction."""

    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    UTILITIES = "utilities"
    SALARY = "salary"
    OTHER = "other"


@dataclass
class Transaction:
    """Represents a single financial transaction."""

    amount: float
    description: str
    category: Category
    transaction_type: TransactionType
    date: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if not self.description.strip():
            raise ValueError("Description cannot be empty")
