# BudgetCLI

A command-line application to track personal income and expenses, categorize transactions, and generate text reports.

Built with Python as a project for the *Quality Development* seminar at UNICT.

---

## Features

- Add income and expense transactions with category
- List all recorded transactions
- Generate a summary report (totals and breakdown by category)
- Delete a transaction by index
- Data persisted locally in a JSON file

## Installation

**Requirements:** Python 3.10+

```bash
git clone https://github.com/GiuseppePitruzzella/budget-cli.git
cd budget-cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

## Usage

```bash
# Add an expense (default type: expense, default category: other)
python3 -m src.budget.cli add 50.0 "Grocery shopping" --category food

# Add an income
python3 -m src.budget.cli add 1500.0 "Monthly salary" --type income --category salary

# List all transactions
python3 -m src.budget.cli list

# Show summary report
python3 -m src.budget.cli report

# Delete a transaction by index
python3 -m src.budget.cli delete 0
```

Available categories: `food`, `transport`, `entertainment`, `health`, `utilities`, `salary`, `other`

By default, transactions are saved to `budget.json` in the current directory. Override with:

```bash
export BUDGET_DATA_FILE=~/.budget/my_budget.json
```

## Running Tests

```bash
pytest --cov src tests/
```

## Project Structure

```
src/budget/
├── models.py    # Transaction dataclass, Category and TransactionType enums
├── storage.py   # JSON persistence layer
├── ledger.py    # In-memory business logic (add, remove, filter, balance)
├── reports.py   # Pure functions: summary, category breakdown, date filter
└── cli.py       # Click CLI commands
tests/
├── test_models.py
├── test_storage.py
├── test_ledger.py
├── test_reports.py
└── test_cli.py
```

## Authors

- Giuseppe Pitruzzella
- Chiara Pitru
