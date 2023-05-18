import csv
import pandas as pd
from files import bought_file


# Report if product already in file
def product_present(file, product_name):
    with open(file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["product_name"] == product_name:
                return True


# Create a new ID if product is not in bought.csv already, otherwise use same ID
def create_id(product_name):
    with open(bought_file, "r") as file:
        reader = csv.reader(file)
        row_count = sum(1 for row in reader) - 1
    df = pd.read_csv(bought_file)
    max_value = df["id"].max()
    if row_count == 0:
        return 1
    elif product_present(bought_file, product_name):
        return bought_id(product_name)
    else:
        return max_value + 1


# Find bought ID's for sold products
def bought_id(product_name):
    with open(bought_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["product_name"] == product_name:
                return row["id"]
