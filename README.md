# Sales Stats CLI

A command-line application built with Python to analyze sales data from a CSV file and generate a statistics report in the terminal and JSON format.

## Features

- Load sales data from CSV files
- Calculate total revenue and number of orders
- Calculate average order value
- Identify top products by revenue
- Calculate revenue by category and month
- Identify the best customer
- Validate input data
- Export results to JSON
- Test functions using pytest

## Technologies

- Python
- CSV and JSON
- argparse
- pytest

## Getting Started

Clone the repository and navigate to the project directory.

Run the application:

```bash
python3 main.py orders.csv --top 3 --out report.json
```

Run the tests:

```bash
python3 -m pytest -v
```

## Project Structure

```text
sales-stats-cli/
├── main.py
├── stats.py
├── orders.csv
├── test_stats.py
└── README.md
```

## Learning Goals

This project demonstrates Python fundamentals, data processing, functions, dictionaries, error handling, command-line arguments, JSON serialization, and automated testing.

## Status

Beginner Python project — actively learning and improving.
