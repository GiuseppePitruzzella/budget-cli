"""Tests for the CLI commands."""

# pylint: disable=redefined-outer-name

from pathlib import Path

import pytest
from click.testing import CliRunner

from src.budget.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def data_file(tmp_path: Path) -> str:
    return str(tmp_path / "test_budget.json")


class TestAddCommand:
    def test_add_exits_with_zero(self, runner: CliRunner, data_file: str) -> None:
        result = runner.invoke(cli, ["add", "50.0", "Coffee", "--data-file", data_file])
        assert result.exit_code == 0

    def test_add_prints_confirmation(self, runner: CliRunner, data_file: str) -> None:
        result = runner.invoke(cli, ["add", "50.0", "Coffee", "--data-file", data_file])
        assert "Coffee" in result.output
        assert "50.00" in result.output

    def test_add_with_category(self, runner: CliRunner, data_file: str) -> None:
        result = runner.invoke(
            cli,
            ["add", "30.0", "Lunch", "--category", "food", "--data-file", data_file],
        )
        assert "food" in result.output

    def test_add_income(self, runner: CliRunner, data_file: str) -> None:
        result = runner.invoke(
            cli,
            ["add", "1000.0", "Salary", "--type", "income", "--data-file", data_file],
        )
        assert "income" in result.output

    def test_add_invalid_amount_fails(self, runner: CliRunner, data_file: str) -> None:
        result = runner.invoke(cli, ["add", "abc", "Test", "--data-file", data_file])
        assert result.exit_code != 0

    def test_add_zero_amount_fails(self, runner: CliRunner, data_file: str) -> None:
        result = runner.invoke(cli, ["add", "0", "Test", "--data-file", data_file])
        assert result.exit_code != 0


class TestListCommand:
    def test_list_empty(self, runner: CliRunner, data_file: str) -> None:
        result = runner.invoke(cli, ["list", "--data-file", data_file])
        assert result.exit_code == 0
        assert "No transactions found" in result.output

    def test_list_shows_added_transaction(
        self, runner: CliRunner, data_file: str
    ) -> None:
        runner.invoke(cli, ["add", "25.0", "Bus ticket", "--data-file", data_file])
        result = runner.invoke(cli, ["list", "--data-file", data_file])
        assert "Bus ticket" in result.output

    def test_list_shows_index(self, runner: CliRunner, data_file: str) -> None:
        runner.invoke(cli, ["add", "25.0", "Bus ticket", "--data-file", data_file])
        result = runner.invoke(cli, ["list", "--data-file", data_file])
        assert "[0]" in result.output


class TestReportCommand:
    def test_report_empty(self, runner: CliRunner, data_file: str) -> None:
        result = runner.invoke(cli, ["report", "--data-file", data_file])
        assert "No transactions found" in result.output

    def test_report_shows_balance(self, runner: CliRunner, data_file: str) -> None:
        runner.invoke(
            cli,
            ["add", "1000.0", "Salary", "--type", "income", "--data-file", data_file],
        )
        runner.invoke(
            cli,
            [
                "add",
                "200.0",
                "Rent",
                "--category",
                "utilities",
                "--data-file",
                data_file,
            ],
        )
        result = runner.invoke(cli, ["report", "--data-file", data_file])
        assert "Balance" in result.output
        assert "800.00" in result.output

    def test_report_shows_category_breakdown(
        self, runner: CliRunner, data_file: str
    ) -> None:
        runner.invoke(
            cli,
            [
                "add",
                "50.0",
                "Groceries",
                "--category",
                "food",
                "--data-file",
                data_file,
            ],
        )
        result = runner.invoke(cli, ["report", "--data-file", data_file])
        assert "food" in result.output


class TestDeleteCommand:
    def test_delete_existing_transaction(
        self, runner: CliRunner, data_file: str
    ) -> None:
        runner.invoke(cli, ["add", "50.0", "Coffee", "--data-file", data_file])
        result = runner.invoke(cli, ["delete", "0", "--data-file", data_file])
        assert result.exit_code == 0
        assert "Deleted" in result.output

    def test_delete_removes_from_list(self, runner: CliRunner, data_file: str) -> None:
        runner.invoke(cli, ["add", "50.0", "Coffee", "--data-file", data_file])
        runner.invoke(cli, ["delete", "0", "--data-file", data_file])
        result = runner.invoke(cli, ["list", "--data-file", data_file])
        assert "No transactions found" in result.output

    def test_delete_invalid_index_fails(
        self, runner: CliRunner, data_file: str
    ) -> None:
        result = runner.invoke(cli, ["delete", "99", "--data-file", data_file])
        assert result.exit_code != 0


class TestListDateFilter:
    def test_list_with_from_date_shows_matching(
        self, runner: CliRunner, data_file: str
    ) -> None:
        runner.invoke(cli, ["add", "10.0", "Recent expense", "--data-file", data_file])
        result = runner.invoke(
            cli, ["list", "--from", "2020-01-01", "--data-file", data_file]
        )
        assert result.exit_code == 0
        assert "Recent expense" in result.output

    def test_list_with_to_date_excludes_future(
        self, runner: CliRunner, data_file: str
    ) -> None:
        runner.invoke(cli, ["add", "10.0", "Some expense", "--data-file", data_file])
        result = runner.invoke(
            cli, ["list", "--to", "1999-12-31", "--data-file", data_file]
        )
        assert "No transactions found" in result.output

    def test_list_with_from_and_to_filters_correctly(
        self, runner: CliRunner, data_file: str
    ) -> None:
        runner.invoke(cli, ["add", "10.0", "Expense today", "--data-file", data_file])
        result = runner.invoke(
            cli,
            [
                "list",
                "--from",
                "2020-01-01",
                "--to",
                "2099-12-31",
                "--data-file",
                data_file,
            ],
        )
        assert "Expense today" in result.output

    def test_invalid_from_date_shows_error(
        self, runner: CliRunner, data_file: str
    ) -> None:
        result = runner.invoke(
            cli, ["list", "--from", "25-11-2025", "--data-file", data_file]
        )
        assert result.exit_code != 0
        assert "YYYY-MM-DD" in result.output

    def test_invalid_to_date_shows_error(
        self, runner: CliRunner, data_file: str
    ) -> None:
        result = runner.invoke(
            cli, ["list", "--to", "not-a-date", "--data-file", data_file]
        )
        assert result.exit_code != 0
        assert "YYYY-MM-DD" in result.output
