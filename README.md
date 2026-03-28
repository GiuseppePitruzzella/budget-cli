# BudgetCLI

**BudgetCLI** is a command-line application written in Python to manage personal finances directly from the terminal. It allows you to record income and expenses, organize them by category, and generate summary reports, all stored locally in a JSON file with no external dependencies.

Built as a group project for the *Quality Development* seminar at UNICT (A.Y. 2025–2026).

---

## Architecture

The application is divided into four independent modules, each with a single responsibility:

| Module | Responsibility |
|---|---|
| `models.py` | Defines `Transaction` (dataclass), `TransactionType` (income/expense) and `Category` (enums) |
| `storage.py` | Reads and writes transactions to a local JSON file via `JSONStorage` |
| `ledger.py` | In-memory business logic: add, remove, filter and balance transactions via `Ledger` |
| `reports.py` | Pure functions for aggregation: summary totals, category breakdown, date range filter |
| `cli.py` | Exposes all features as terminal commands using [Click](https://click.palletsprojects.com/) |

The CLI layer coordinates the others: it loads data from `JSONStorage`, operates on a `Ledger` instance, then persists the result back. `Ledger` and `reports` have no knowledge of files or I/O, making them straightforward to test.

```
src/budget/
├── __init__.py
├── models.py
├── storage.py
├── ledger.py
├── reports.py
└── cli.py
tests/
├── test_models.py
├── test_storage.py
├── test_ledger.py
├── test_reports.py
└── test_cli.py
```

---

## Installation

**Requirements:** Python 3.10+

```bash
git clone https://github.com/GiuseppePitruzzella/budget-cli.git
cd budget-cli

python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install -r requirements_dev.txt
```

---

## Usage

All commands follow the pattern `python3 -m src.budget.cli <command> [options]`.

### Add a transaction

```bash
# Expense (default type and category)
python3 -m src.budget.cli add 50.0 "Grocery shopping"

# Expense with category
python3 -m src.budget.cli add 12.50 "Bus monthly pass" --category transport

# Income
python3 -m src.budget.cli add 1500.0 "Monthly salary" --type income --category salary
```

**Available categories:** `food`, `transport`, `entertainment`, `health`, `utilities`, `salary`, `other`

### List all transactions

```bash
# List all transactions
python3 -m src.budget.cli list

# Filter by date range
python3 -m src.budget.cli list --from 2025-11-01 --to 2025-11-30

# Filter by category
python3 -m src.budget.cli list --category food

# Combine filters
python3 -m src.budget.cli list --category transport --from 2025-11-01
```

Output example:

```
[0] 2025-11-01 | Monthly salary       | € 1500.00 | salary          | income
[1] 2025-11-03 | Grocery shopping     | €   50.00 | other           | expense
[2] 2025-11-05 | Bus monthly pass     | €   12.50 | transport       | expense
```

### Generate a report

```bash
python3 -m src.budget.cli report
```

Output example:

```
Transactions :  3
Total income : €1500.00
Total expenses: €62.50
Balance      : €1437.50

By category:
  salary          €1500.00
  other           €50.00
  transport       €12.50
```

### Delete a transaction

```bash
# Delete the transaction at index 1 (use 'list' to find the index)
python3 -m src.budget.cli delete 1
```

### Custom data file

By default, transactions are saved to `budget.json` in the current directory. You can override this with an environment variable:

```bash
export BUDGET_DATA_FILE=~/.budget/my_budget.json
python3 -m src.budget.cli list
```

---

## Running tests

```bash
# Run all tests with coverage report
pytest --cov src tests/

# Run a specific test file
pytest tests/test_ledger.py -v
```

The test suite covers **100% of the source code** across 76 tests.

---

## Authors

- Giuseppe Pitruzzella
- Chiara Pitruzzella
