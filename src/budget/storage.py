"""JSON persistence layer for BudgetCLI transactions."""

import json
from datetime import date
from pathlib import Path
from typing import Any

from src.budget.models import Category, Transaction, TransactionType


def _transaction_to_dict(transaction: Transaction) -> dict[str, Any]:
    return {
        "amount": transaction.amount,
        "description": transaction.description,
        "category": transaction.category.value,
        "transaction_type": transaction.transaction_type.value,
        "date": transaction.date.isoformat(),
    }


def _dict_to_transaction(data: dict[str, Any]) -> Transaction:
    return Transaction(
        amount=data["amount"],
        description=data["description"],
        category=Category(data["category"]),
        transaction_type=TransactionType(data["transaction_type"]),
        date=date.fromisoformat(data["date"]),
    )


class JSONStorage:
    """Handles reading and writing transactions to a JSON file."""

    def __init__(self, filepath: str) -> None:
        self._path = Path(filepath)

    def load(self) -> list[Transaction]:
        """Load all transactions from the JSON file.

        Returns an empty list if the file does not exist.
        """
        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as f:
            raw: list[dict[str, Any]] = json.load(f)
        return [_dict_to_transaction(item) for item in raw]

    def save(self, transactions: list[Transaction]) -> None:
        """Persist a list of transactions to the JSON file."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as f:
            json.dump([_transaction_to_dict(t) for t in transactions], f, indent=2)
