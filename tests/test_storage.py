"""Tests for the JSON persistence layer."""

from datetime import date
from pathlib import Path

import pytest

from src.budget.models import Category, Transaction, TransactionType
from src.budget.storage import JSONStorage


@pytest.fixture
def storage(tmp_path: Path) -> JSONStorage:
    return JSONStorage(str(tmp_path / "transactions.json"))


@pytest.fixture
def sample_transaction() -> Transaction:
    return Transaction(
        amount=42.0,
        description="Lunch",
        category=Category.FOOD,
        transaction_type=TransactionType.EXPENSE,
        date=date(2025, 11, 1),
    )


class TestJSONStorageLoad:
    """Tests for the load method."""

    def test_load_returns_empty_list_when_file_missing(
        self, storage: JSONStorage
    ) -> None:
        assert storage.load() == []

    def test_load_returns_saved_transactions(
        self, storage: JSONStorage, sample_transaction: Transaction
    ) -> None:
        storage.save([sample_transaction])
        loaded = storage.load()
        assert len(loaded) == 1

    def test_load_preserves_amount(
        self, storage: JSONStorage, sample_transaction: Transaction
    ) -> None:
        storage.save([sample_transaction])
        assert storage.load()[0].amount == sample_transaction.amount

    def test_load_preserves_description(
        self, storage: JSONStorage, sample_transaction: Transaction
    ) -> None:
        storage.save([sample_transaction])
        assert storage.load()[0].description == sample_transaction.description

    def test_load_preserves_category(
        self, storage: JSONStorage, sample_transaction: Transaction
    ) -> None:
        storage.save([sample_transaction])
        assert storage.load()[0].category == sample_transaction.category

    def test_load_preserves_transaction_type(
        self, storage: JSONStorage, sample_transaction: Transaction
    ) -> None:
        storage.save([sample_transaction])
        assert storage.load()[0].transaction_type == sample_transaction.transaction_type

    def test_load_preserves_date(
        self, storage: JSONStorage, sample_transaction: Transaction
    ) -> None:
        storage.save([sample_transaction])
        assert storage.load()[0].date == sample_transaction.date


class TestJSONStorageSave:
    """Tests for the save method."""

    def test_save_creates_file(
        self, storage: JSONStorage, sample_transaction: Transaction
    ) -> None:
        storage.save([sample_transaction])
        assert Path(storage._path).exists()

    def test_save_multiple_transactions(self, storage: JSONStorage) -> None:
        transactions = [
            Transaction(
                amount=10.0,
                description="Coffee",
                category=Category.FOOD,
                transaction_type=TransactionType.EXPENSE,
                date=date(2025, 11, 1),
            ),
            Transaction(
                amount=2000.0,
                description="Salary",
                category=Category.SALARY,
                transaction_type=TransactionType.INCOME,
                date=date(2025, 11, 1),
            ),
        ]
        storage.save(transactions)
        loaded = storage.load()
        assert len(loaded) == 2

    def test_save_overwrites_existing_data(
        self, storage: JSONStorage, sample_transaction: Transaction
    ) -> None:
        storage.save([sample_transaction])
        storage.save([])
        assert storage.load() == []
