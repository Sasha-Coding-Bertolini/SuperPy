from reports import report_inventory, report_revenue, report_profit
import pandas as pd
from date import manipulate_date
from files import current_directory, inventory_file
import os
from unittest.mock import patch


# Sample data for testing
inventory_data = {
    "id": [1, 2, 3],
    "product_name": ["Product A", "Product B", "Product C"],
    "count": [10, 20, 30],
    "buy_price": [5.99, 9.99, 14.99],
    "expiration_date": ["2023-12-31", "2023-12-31", "2023-12-31"],
    "buy_date": ["2023-01-01", "2023-01-02", "2023-01-03"],
}


def test_report_inventory():
    # Create a test DataFrame from sample data
    df = pd.DataFrame(inventory_data)

    # Mock the read_csv function to return the test DataFrame
    pd_read_csv_mock = lambda _: df

    # Test case 1: Testing num_days_inventory branch
    with patch("pandas.read_csv", pd_read_csv_mock):
        selected_rows = report_inventory(inventory_file, None, 2, None, None)
        expected_rows = df[df["buy_date"] <= manipulate_date(2)].drop(
            "buy_date", axis=1
        )
        assert selected_rows.equals(expected_rows)

    # Test case 2: Testing year branch
    with patch("pandas.read_csv", pd_read_csv_mock):
        selected_rows = report_inventory(inventory_file, None, None, 2023, None)
        expected_rows = df[
            (df["buy_date"] >= "2023-01-01") & (df["buy_date"] <= "2023-12-31")
        ].drop("buy_date", axis=1)
        assert selected_rows.equals(expected_rows)

    # Test case 3: Testing year and month branch
    with patch("pandas.read_csv", pd_read_csv_mock):
        selected_rows = report_inventory(inventory_file, None, None, 2023, 1)
        expected_rows = df[
            (df["buy_date"] >= "2023-01-01") & (df["buy_date"] <= "2023-01-31")
        ].drop("buy_date", axis=1)
        assert selected_rows.equals(expected_rows)

    # Test case 4: Testing date_inventory branch
    with patch("pandas.read_csv", pd_read_csv_mock):
        selected_rows = report_inventory(inventory_file, "2023-01-02", None, None, None)
        expected_rows = df[df["buy_date"] <= "2023-01-02"].drop("buy_date", axis=1)
        assert selected_rows.equals(expected_rows)


def test_report_revenue():
    # test data in file:
    test_sold_file = os.path.join(current_directory, r"test_sold.csv")

    # Test case 1: Testing today branch
    expected_revenue_today = (
        0.0  # Expected revenue value for today based on data in "test_sold.csv"
    )
    revenue_today = report_revenue(test_sold_file, None, None, None, None, today=True)
    assert revenue_today == expected_revenue_today

    # Test case 2: Testing year branch
    expected_revenue_year = 122  # Expected revenue value for year
    revenue_year = report_revenue(test_sold_file, None, None, 2023, None, today=False)
    assert revenue_year == expected_revenue_year

    # Test case 3: Testing year and month branch
    expected_revenue_year_month = 122  # Expected revenue value for year and month
    revenue_year_month = report_revenue(
        test_sold_file, None, None, 2023, 5, today=False
    )
    assert revenue_year_month == expected_revenue_year_month

    # Test case 4: Testing current_date branch
    expected_revenue_current_date = 110  # Expected revenue value on specific date
    revenue_current_date = report_revenue(
        test_sold_file, "2023-05-16", None, None, None, today=False
    )
    assert revenue_current_date == expected_revenue_current_date


def test_report_profit():
    test_sold_file = os.path.join(current_directory, r"test_sold.csv")
    test_bought_file = os.path.join(current_directory, r"test_bought.csv")
    # Test case 1: Testing today branch
    expected_profit_today = 0.0
    profit_today = report_profit(
        test_bought_file, test_sold_file, None, None, None, None, True
    )
    assert profit_today == expected_profit_today

    # Test case 2: Testing year branch
    expected_profit_year = 28.4
    profit_year = report_profit(
        test_bought_file, test_sold_file, None, None, 2023, None, None
    )
    assert profit_year == expected_profit_year

    # Test case 3: Testing year and month branch
    expected_profit_year_month = 28.4
    profit_year_month = report_profit(
        test_bought_file, test_sold_file, None, None, 2023, 5, None
    )
    assert profit_year_month == expected_profit_year_month

    # Test case 4: Testing current_date branch
    expected_profit_current_date = 110
    profit_current_date = report_profit(
        test_bought_file, test_sold_file, "2023-05-16", None, None, None, None
    )
    assert profit_current_date == expected_profit_current_date
