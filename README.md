# SuperPy

A command-line tool written in Python 3 that supermarkets use to keep track of their inventory.

## Used Modules

- argparse (https://docs.python.org/3/library/argparse.html)
- calendar (https://docs.python.org/3/library/calendar.html)
- csv (https://docs.python.org/3/library/csv.html)
- re (https://docs.python.org/3/library/re.html)
- datetime (https://docs.python.org/3/library/datetime.html)
- os.path (https://docs.python.org/3/library/os.path.html)
- rich (https://rich.readthedocs.io/en/stable/introduction.html)
  - `pip install rich`
- unittest.mock (https://docs.python.org/3/library/unittest.html)
- pandas (https://pandas.pydata.org/)
  - `pip install pandas`
- pytest (https://docs.pytest.org/en/7.3.x/)
  - `pip install -U pytest`

## Commandline Options

- `pytest`

Performs a test on testfiles in program. Perform test to verify if report functions work correctly.

- `python super.py -h` or `python super.py --help`

```
usage: super.py [-h] [--product-name PRODUCT_NAME] [--buy-price BUY_PRICE] [--sell-price SELL_PRICE]
[--expiration-date EXPIRATION_DATE] [--now] [--yesterday] [--today] [--date DATE]
[--advance-date ADVANCE_DATE]
[{buy,sell,report inventory,report profit,report revenue}]

Perform action to buy and sell products and to report on supermarket inventory, revenue and profit

positional arguments:
{buy,sell,report inventory,report profit,report revenue}
Action to perform

options:
-h, --help: show this help message and exit
--product-name: name of the product to buy or sell
--buy-price: buy price of the bought product
--sell-price: sell price of the sold product
--expiration-date: expiration date of the product in the format YYYY-MM-DD
--now: Provide reports up until now
--yesterday: Provide reports of yesterday
--today: Provide reports of today
--date: Provide report of a specific time frame in format YYYY, or YYYY-MM, or YYYY-MM-DD
--advance-date: Advance the date by number of days, or reset
```

### `--advance-date`

The internal conception of what day it is. Use `--advance-date reset` to reset the internal day to today’s date. The date does not automatically set to today's date when starting the program, so remember to reset the date if you want to start with today's date. This option does not require other arguments.

- `python super.py --advance-date 2`
- `python super.py --advance-date 5`
- `python super.py --advance-date reset`

### `--set-date`

Sets the date to a specific date. Takes a date in format YYYY-MM-DD.

- `python super.py --set-date 2023-01-01`

### `buy`

Record buys of products with `buy` and provide `product-name` (short name, lowercase, without spaces), `buy-price` and `expiration-date`.

- `python super.py buy --product-name orange --buy-price 0.8 --expiration-date 2020-05-01`
- `python super.py buy --product-name peach --buy-price 2.25 --expiration-date 2020-08-01`

### `sell`

Record sells of products with `sell` and provide `product-name` (short name, lowercase, without spaces) and `sell-price`.

- `python super.py sell --product-name orange --sell-price 2`
- `python super.py sell --product-name peach --sell-price 3.95`

### `report inventory`

Report inventory with `report inventory` and provide a time argument.

- `python super.py 'report inventory' --now`
- `python super.py 'report inventory' --yesterday`
- `python super.py 'report inventory' --date 2023`
- `python super.py 'report inventory' --date 2023-05`
- `python super.py 'report inventory' --date 2023-04-12`

### `report revenue`

Report revenue with `report revenue` and provide a required time argument.

- `python super.py 'report revenue' --now`
- `python super.py 'report revenue' --today`
- `python super.py 'report revenue' --yesterday`
- `python super.py 'report revenue' --date 2021`
- `python super.py 'report revenue' --date 2021-06`
- `python super.py 'report revenue' --date 2021-06-02`

### `report profit`

Report revenue with `report profit` and provide a required time argument.

- `python super.py 'report profit' --now`
- `python super.py 'report profit' --today`
- `python super.py 'report profit' --yesterday`
- `python super.py 'report profit' --date 2023`
- `python super.py 'report profit' --date 2022-06`
- `python super.py 'report profit' --date 2023-05-02`
