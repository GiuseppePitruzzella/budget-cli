"""CLI entry point for BudgetCLI."""

import os
from datetime import date

import click

from src.budget.ledger import Ledger
from src.budget.models import Category, Transaction, TransactionType
from src.budget.reports import (
    breakdown_by_category,
    filter_by_date_range,
    generate_summary,
)
from src.budget.storage import JSONStorage

DEFAULT_DATA_FILE = os.environ.get("BUDGET_DATA_FILE", "budget.json")


def _parse_date(value: str, option_name: str) -> date:
    """Parse a YYYY-MM-DD string, raising a user-friendly error on failure."""
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise click.BadParameter(
            f"'{value}' is not a valid date. Expected format: YYYY-MM-DD.",
            param_hint=f"'--{option_name}'",
        ) from exc


_CATEGORY_CHOICES = [c.value for c in Category]
_TYPE_CHOICES = [t.value for t in TransactionType]


def _get_ledger(data_file: str) -> tuple[Ledger, JSONStorage]:
    storage = JSONStorage(data_file)
    return Ledger(storage.load()), storage


@click.group()
def cli() -> None:
    """BudgetCLI — Personal budget manager from the terminal."""


@cli.command()
@click.argument("amount", type=float)
@click.argument("description")
@click.option(
    "--category",
    "-c",
    type=click.Choice(_CATEGORY_CHOICES),
    default="other",
    show_default=True,
)
@click.option(
    "--type",
    "-t",
    "transaction_type",
    type=click.Choice(_TYPE_CHOICES),
    default="expense",
    show_default=True,
)
@click.option("--data-file", default=DEFAULT_DATA_FILE, hidden=True)
def add(
    amount: float,
    description: str,
    category: str,
    transaction_type: str,
    data_file: str,
) -> None:
    """Add a new income or expense transaction."""
    ledger, storage = _get_ledger(data_file)
    transaction = Transaction(
        amount=amount,
        description=description,
        category=Category(category),
        transaction_type=TransactionType(transaction_type),
        date=date.today(),
    )
    ledger.add(transaction)
    storage.save(ledger.all())
    click.echo(f"Added: {description} — €{amount:.2f} [{category}/{transaction_type}]")


@cli.command("list")
@click.option(
    "--from",
    "date_from",
    default=None,
    help="Show transactions from this date (YYYY-MM-DD).",
)
@click.option(
    "--to",
    "date_to",
    default=None,
    help="Show transactions up to this date (YYYY-MM-DD).",
)
@click.option(
    "--category",
    "-c",
    "filter_category",
    type=click.Choice(_CATEGORY_CHOICES),
    default=None,
    help="Show only transactions of this category.",
)
@click.option("--data-file", default=DEFAULT_DATA_FILE, hidden=True)
def list_transactions(
    date_from: str | None,
    date_to: str | None,
    filter_category: str | None,
    data_file: str,
) -> None:
    """List all recorded transactions, optionally filtered by date or category."""
    ledger, _ = _get_ledger(data_file)
    transactions = ledger.all()
    if date_from is not None or date_to is not None:
        start = _parse_date(date_from, "from") if date_from else date.min
        end = _parse_date(date_to, "to") if date_to else date.max
        transactions = filter_by_date_range(transactions, start, end)
    if filter_category is not None:
        cat = Category(filter_category)
        transactions = [t for t in transactions if t.category == cat]
    if not transactions:
        click.echo("No transactions found.")
        return
    for i, t in enumerate(transactions):
        click.echo(
            f"[{i}] {t.date} | {t.description:20s} | €{t.amount:>8.2f}"
            f" | {t.category.value:15s} | {t.transaction_type.value}"
        )


@cli.command()
@click.option("--data-file", default=DEFAULT_DATA_FILE, hidden=True)
def report(data_file: str) -> None:
    """Show a summary report of all transactions."""
    ledger, _ = _get_ledger(data_file)
    transactions = ledger.all()
    if not transactions:
        click.echo("No transactions found.")
        return
    s = generate_summary(transactions)
    click.echo(f"Transactions : {s.transaction_count}")
    click.echo(f"Total income : €{s.total_income:.2f}")
    click.echo(f"Total expenses: €{s.total_expenses:.2f}")
    click.echo(f"Balance      : €{s.balance:.2f}")
    click.echo("\nBy category:")
    for cat, total in breakdown_by_category(transactions).items():
        click.echo(f"  {cat.value:15s} €{total:.2f}")


@cli.command()
@click.argument("index", type=int)
@click.option("--data-file", default=DEFAULT_DATA_FILE, hidden=True)
def delete(index: int, data_file: str) -> None:
    """Delete a transaction by its index (see 'list')."""
    ledger, storage = _get_ledger(data_file)
    try:
        removed = ledger.remove(index)
        storage.save(ledger.all())
        click.echo(f"Deleted: {removed.description} — €{removed.amount:.2f}")
    except IndexError as exc:
        click.echo(f"Error: no transaction at index {index}.", err=True)
        raise SystemExit(1) from exc


if __name__ == "__main__":  # pragma: no cover
    cli()
