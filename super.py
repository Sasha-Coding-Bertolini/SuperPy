import argparse
from bought import Bought
from sold import Sold
from products import product_present
from files import inventory_file, sold_file, bought_file
from reports import report_inventory, report_profit, report_revenue
from date import update_date, read_date, reset_date, set_date
import calendar
from rich import print
import re

parser = argparse.ArgumentParser(
    description="Perform action to buy and sell products and to report on supermarket inventory, revenue and profit"
)

parser.add_argument(
    "action",
    type=str,
    nargs="?",
    help="Action to perform",
    choices=[
        "buy",
        "sell",
        "report inventory",
        "report profit",
        "report revenue",
    ],
    const=None,
    default=None,
)

parser.add_argument("--product-name", type=str, help="Name of the product to buy")
parser.add_argument("--buy-price", type=float, help="Buy price of the product")
parser.add_argument("--sell-price", type=float, help="Sell price of the product")
parser.add_argument(
    "--expiration-date",
    type=str,
    help="Expiration date of the product in the format YYYY-MM-DD",
)
parser.add_argument("--now", action="store_true", help="Provide reports of today")
parser.add_argument(
    "--yesterday", action="store_true", help="Provide reports of yesterday"
)
parser.add_argument("--today", action="store_true", help="Provide reports of today")
parser.add_argument(
    "--date", type=str, help="Date of report in format YYYY, or YYYY-MM, or YYYY-MM-DD"
)
parser.add_argument(
    "--advance-date",
    type=lambda x: int(x) if x.isdigit() else x.lower(),
    help="Advance the date, or reset",
)
parser.add_argument(
    "--set-date",
    type=str,
    help="Set the date to a specific date in format YYY-MM-DD",
)


args = parser.parse_args()

if args.set_date:
    if re.match(r"\d{4}-\d{2}-\d{2}", args.set_date):
        # Valid date format, proceed with the code
        set_date(args.set_date)
        print(f"The date has been set to {args.set_date}.")
    else:
        print("Invalid date format. Please use YYYY-MM-DD format.")


if args.advance_date:
    if str(args.advance_date).lstrip("-").isdigit():
        update_date(int(args.advance_date))
    elif args.advance_date == "reset":
        reset_date()
        print(f"[bold]The date has been reset to {read_date()}[/bold]")
    else:
        print(
            "[bold red]Error[/bold red]: You must provide an integer value to advance the time or reset to the current date."
        )


if args.action == "buy":
    if not args.product_name:
        print("[bold red]Error[/bold red]: Product name is required")
    elif not args.buy_price:
        print("[bold red]Error[/bold red]: Buy price is required")
    elif not args.expiration_date:
        print("[bold red]Error[/bold red]: Expiration date is required")
    else:
        print(
            f"Buying {args.product_name} for {args.buy_price} euro with an expiration date of {args.expiration_date}."
        )
        buy_product = Bought(args.product_name, args.buy_price, args.expiration_date)
        buy_product.buy()

if args.action == "sell":
    if not args.product_name:
        print("[bold red]Error[/bold red]: Product name is required")
    elif not args.sell_price:
        print("[bold red]Error[/bold red]: Sell price is required")
    elif not product_present(inventory_file, args.product_name):
        print(
            f"{args.product_name} cannot be sold, because it is not in the inventory."
        )
    else:
        print(f"Selling {args.product_name} for {args.sell_price} euro.")
        sell_product = Sold(args.product_name, args.sell_price)
        sell_product.sell()

# Create argument using this function: def report_inventory(file, date_inventory, num_days_inventory, year, month)
if args.action == "report inventory":
    if args.now:
        report_inventory(inventory_file, read_date(), None, None, None)
    elif args.yesterday:
        report_inventory(inventory_file, None, 1, None, None)
    elif args.date:
        if len(args.date) == 4:
            report_inventory(inventory_file, None, None, args.date, None)
        elif len(args.date) > 4 and len(args.date) < 8:
            year = str(args.date).split("-")[0]
            month = str(args.date).split("-")[1]
            report_inventory(inventory_file, None, None, year, month)
        else:
            report_inventory(inventory_file, args.date, None, None, None)
    else:
        print(
            "[bold red]Error[/bold red]: you must give a timeframe for the inventory report"
        )

# Create argument using this function: def report_revenue(file, current_date, num_days_revenue, year, month, today)
if args.action == "report revenue":
    if args.now:
        print(
            "The total revenue so far is: "
            + str(report_revenue(sold_file, read_date(), None, None, None, None))
            + " euro."
        )

    elif args.yesterday:
        print(
            "Yesterday's revenue was: "
            + str(report_revenue(sold_file, None, 1, None, None, None))
            + " euro."
        )

    elif args.today:
        print(
            "Today's revenue is: "
            + str(report_revenue(sold_file, None, None, None, None, True))
            + " euro."
        )
    elif args.date:
        if len(args.date) == 4:
            print(
                f"The revenue in {args.date} was "
                + str(report_revenue(sold_file, None, None, args.date, None, None))
                + " euro."
            )

        elif len(args.date) > 4 and len(args.date) < 8:
            year = str(args.date).split("-")[0]
            month = str(args.date).split("-")[1]
            month_name = calendar.month_name[month]
            print(
                f"The revenue in {month_name}, {year} was "
                + str(report_revenue(sold_file, None, None, year, month, None))
                + " euro."
            )

        else:
            print(
                f"The revenue on {args.date} was: "
                + str(report_revenue(sold_file, args.date, None, None, None, None))
                + " euro."
            )

    else:
        print(
            "[bold red]Error[/bold red]: you must give a timeframe for the revenue report"
        )

# Create argument using this function: def report_profit(file, revenue_file, current_date, num_days_profit, year, month, today):
if args.action == "report profit":
    if args.now:
        print(
            "The total profit so far is: "
            + str(
                report_profit(
                    bought_file, sold_file, read_date(), None, None, None, None
                )
            )
            + " euro."
        )
    elif args.yesterday:
        print(
            "Yesterday's profit was: "
            + str(report_profit(bought_file, sold_file, None, 1, None, None, None))
            + " euro."
        )

    elif args.today:
        print(
            "Today's profit is: "
            + str(report_profit(bought_file, sold_file, None, None, None, None, True))
            + " euro."
        )

    elif args.date:
        if len(args.date) == 4:
            print(
                f"The total profit in {args.date} was: "
                + str(
                    report_profit(
                        bought_file, sold_file, None, None, args.date, None, None
                    )
                )
                + " euro."
            )

        elif len(args.date) > 4 and len(args.date) < 8:
            year = str(args.date).split("-")[0]
            month = str(args.date).split("-")[1]
            month_name = calendar.month_name[int(month)]
            print(
                f"The total profit in {month_name}, {year} was: "
                + str(
                    report_profit(bought_file, sold_file, None, None, year, month, None)
                )
                + " euro."
            )

        else:
            print(
                f"The total profit on {args.date} was: "
                + str(
                    report_profit(
                        bought_file, sold_file, args.date, None, None, None, None
                    )
                )
                + " euro."
            )
    else:
        print(
            "[bold red]Error[/bold red]: you must give a timeframe for the profit report"
        )
