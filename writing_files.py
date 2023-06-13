from files import bought_file, inventory_file, sold_file
from products import product_present, same_buy_date, same_expiration_date
import csv
import pandas as pd


# Create function for writing bought.csv
def write_bought_file(write_values):
    with open(bought_file, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "product_name",
                "buy_date",
                "buy_price",
                "expiration_date",
            ],
        )
        writer.writerow(
            {
                "id": write_values[0],
                "product_name": write_values[1],
                "buy_date": write_values[2],
                "buy_price": write_values[3],
                "expiration_date": write_values[4],
            }
        )


# Create function for writing sold.csv
def write_sold_file(write_values):
    with open(sold_file, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "product_name", "sell_date", "sell_price"],
        )
        if product_present(inventory_file, write_values[1]):
            writer.writerow(
                {
                    "id": write_values[0],
                    "product_name": write_values[1],
                    "sell_date": write_values[2],
                    "sell_price": write_values[3],
                }
            )
        else:
            return "This product cannot be sold because it is not in the inventory."


# Create function for adding bought products to inventory.csv
def add_inventory_product(write_values):
    df = pd.read_csv(inventory_file)
    # Add count if product already in inventory, buy_date is the same and expiration_date is the same
    if (
        product_present(inventory_file, write_values[1])
        and same_buy_date(inventory_file, write_values[5])
        and same_expiration_date(inventory_file, write_values[4])
    ):
        df.loc[
            (df["product_name"] == write_values[1])
            & (df["buy_date"] == write_values[5])
            & (df["expiration_date"] == write_values[4]),
            "count",
        ] += 1

        df.to_csv(inventory_file, index=False)
    # Add new product to inventory if not present
    else:
        new_row = {
            "id": write_values[0],
            "product_name": write_values[1],
            "count": write_values[2],
            "buy_price": write_values[3],
            "expiration_date": write_values[4],
            "buy_date": write_values[5],
        }
        df.loc[len(df)] = new_row
        df.to_csv(inventory_file, index=False)


# Create function for removing sold products from inventory.csv
def remove_inventory_product(product_name):
    df = pd.read_csv(inventory_file)
    # Report unable to sell if product not in inventory
    if not product_present(inventory_file, product_name):
        return f"{product_name} cannot be sold because it is not in the inventory."
    # if product is in inventory and count == 1, then delete product from inventory
    elif product_present(inventory_file, product_name) and (
        df.loc[df["product_name"] == product_name, "count"].iloc[0] == 1
    ):
        print(f"{product_name} is present in inventory, subtracting count -1")
        df = df.drop(df.loc[df["product_name"] == product_name].index[0])
        df.to_csv(inventory_file, index=False)
    # Subtract count if product already in inventory
    else:
        print(f"{product_name} is present in inventory, subtracting count -1")
        subtracted_count = False  # Flag variable to track if count has been subtracted
        for index, row in df.iterrows():
            if row["product_name"] == product_name and not subtracted_count:
                df.loc[index, "count"] = row["count"] - 1
                subtracted_count = (
                    True  # Set flag to True after subtracting count for the first row
                )
        df.to_csv(inventory_file, index=False)
