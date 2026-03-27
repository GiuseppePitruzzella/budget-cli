"""Core business logic for managing a list of transactions."""

from src.budget.models import Category, Transaction, TransactionType


class Ledger:
    """Manages a collection of transactions in memory."""

    def __init__(self, transactions: list[Transaction] | None = None) -> None:
        self._transactions: list[Transaction] = transactions or []

    def add(self, transaction: Transaction) -> None:
        """Append a transaction to the ledger."""
        self._transactions.append(transaction)

    def remove(self, index: int) -> Transaction:
        """Remove and return the transaction at the given index.

        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index >= len(self._transactions):
            raise IndexError(f"No transaction at index {index}")
        return self._transactions.pop(index)

    def all(self) -> list[Transaction]:
        """Return a copy of all transactions."""
        return list(self._transactions)

    def filter_by_category(self, category: Category) -> list[Transaction]:
        """Return transactions matching the given category."""
        return [t for t in self._transactions if t.category == category]

    def filter_by_type(self, transaction_type: TransactionType) -> list[Transaction]:
        """Return transactions matching the given type (income or expense)."""
        return [t for t in self._transactions if t.transaction_type == transaction_type]

    def balance(self) -> float:
        """Return the net balance: sum of incomes minus sum of expenses."""
        total = 0.0
        for t in self._transactions:
            if t.transaction_type == TransactionType.INCOME:
                total += t.amount
            else:
                total -= t.amount
        return total
