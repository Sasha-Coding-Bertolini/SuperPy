import pandas as pd
from date import read_date, manipulate_date
import calendar
from rich.console import Console
from rich.table import Table


def main():
    ...


# Create function for styling the inventory report using Rich module:
def print_table(data):
    # Get the column names from the DataFrame
    header = data.columns.tolist()

    # Create a table
    table = Table(show_header=True, header_style="bold magenta")

    # Add columns based on the header
    for column in header:
        table.add_column(column)

    # Populate the table with data
    for _, row in data.iterrows():
        table.add_row(*[str(value) for value in row])

    # Create a console and print the table
    console = Console()
    console.print(table)


# Create functions for providing reports.
# REPORT INVENTORY:
def report_inventory(file, date_inventory, num_days_inventory, year, month):
    df = pd.read_csv(file)
    # Convert 'date' column to datetime format
    df["buy_date"] = pd.to_datetime(df["buy_date"])

    if num_days_inventory:
        # Select rows before the given date
        selected_rows = df[df["buy_date"] <= manipulate_date(num_days_inventory)]
    elif year and not month:
        date_range = pd.date_range(start=f"{str(year)}-01-01", end=f"{str(year)}-12-31")
        selected_rows = df[df["buy_date"].isin(date_range)]
    elif year and month:
        year = int(year)
        month = int(month)
        days_in_month = calendar.monthrange(year, month)[1]
        date_range = pd.date_range(
            start=f"{str(year)}-{str(month)}-01",
            end=f"{str(year)}-{str(month)}-{str(days_in_month)}",
        )
        selected_rows = df[df["buy_date"].isin(date_range)]
    else:
        # Select rows before the given date
        selected_rows = df[df["buy_date"] <= date_inventory]

    # Reset the index of selected_rows
    selected_rows = selected_rows.reset_index(drop=True)

    # Drop the 'buy_date' column from the DataFrame
    selected_rows = selected_rows.drop(columns=["buy_date"])

    # Merge rows with the same product_name and update the count column
    selected_rows = selected_rows.groupby(
        ["product_name", "expiration_date"], as_index=False
    ).agg(
        {
            "id": "first",
            "buy_price": "first",
            "expiration_date": "first",
            "count": "sum",
        }
    )

    # Reorder the columns
    selected_rows = selected_rows[
        ["id", "product_name", "count", "buy_price", "expiration_date"]
    ]

    # Sort rows based on 'id' column in ascending order
    selected_rows = selected_rows.sort_values("id", ascending=True)

    print_table(selected_rows)
    return selected_rows


# REPORT REVENUE:
def report_revenue(file, current_date, num_days_revenue, year, month, today):
    df = pd.read_csv(file)
    # convert 'date' column to datetime format
    df["sell_date"] = pd.to_datetime(df["sell_date"])
    if today:
        # select rows before on current date
        selected_rows = df[df["sell_date"] == read_date()]
        # add al the selling prices of selected rows
        return selected_rows["sell_price"].sum()
    if num_days_revenue:
        # select rows before the given date
        selected_rows = df[df["sell_date"] <= manipulate_date(num_days_revenue)]
        # add al the selling prices of selected rows

        return selected_rows["sell_price"].sum()
    elif year and not month:
        date_range = pd.date_range(start=f"{str(year)}-01-01", end=f"{str(year)}-12-31")
        selected_rows = df[df["sell_date"].isin(date_range)]

        return selected_rows["sell_price"].sum()
    elif year and month:
        year = int(year)
        month = int(month)
        days_in_month = calendar.monthrange(year, month)[1]
        date_range = pd.date_range(
            start=f"{str(year)}-{str(month)}-01",
            end=f"{str(year)}-{str(month)}-{str(days_in_month)}",
        )
        selected_rows = df[df["sell_date"].isin(date_range)]

        return selected_rows["sell_price"].sum()
    else:
        # select rows on the given date
        selected_rows = df[df["sell_date"] == current_date]
        # add al the selling prices of selected rows

        return selected_rows["sell_price"].sum()


# REPORT PROFIT:
def report_profit(
    file, revenue_file, current_date, num_days_profit, year, month, today
):
    revenue = report_revenue(
        revenue_file, current_date, num_days_profit, year, month, today
    )
    df = pd.read_csv(file)
    # convert 'date' column to datetime format
    df["buy_date"] = pd.to_datetime(df["buy_date"])
    if today:
        # select rows before on current date
        selected_rows = df[df["buy_date"] == read_date()]
        # add all the buying prices of selected rows
        costs = selected_rows["buy_price"].sum()
        return revenue - costs
    elif num_days_profit:
        # select rows before the given date
        selected_rows = df[df["buy_date"] <= manipulate_date(num_days_profit)]
        # add al the buying prices of selected rows
        costs = selected_rows["buy_price"].sum()
        return round((revenue - costs), 2)

    elif year and not month:
        date_range = pd.date_range(start=f"{str(year)}-01-01", end=f"{str(year)}-12-31")
        selected_rows = df[df["buy_date"].isin(date_range)]
        costs = selected_rows["buy_price"].sum()
        return round((revenue - costs), 2)

    elif year and month:
        year = int(year)
        month = int(month)
        days_in_month = calendar.monthrange(year, month)[1]
        date_range = pd.date_range(
            start=f"{str(year)}-{str(month)}-01",
            end=f"{str(year)}-{str(month)}-{str(days_in_month)}",
        )
        selected_rows = df[df["buy_date"].isin(date_range)]

        costs = selected_rows["buy_price"].sum()
        return round((revenue - costs), 2)

    else:
        # select rows before the given date
        selected_rows = df[df["buy_date"] == current_date]
        # add al the buying prices of selected rows
        costs = selected_rows["buy_price"].sum()
        return round((revenue - costs), 2)


if __name__ == "__main__":
    main()
