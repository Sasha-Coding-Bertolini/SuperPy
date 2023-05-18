import os
import pandas as pd

# Create variables for files
current_directory = os.path.dirname(__file__)
bought_file = os.path.join(current_directory, r"bought.csv")
sold_file = os.path.join(current_directory, r"sold.csv")
inventory_file = os.path.join(current_directory, r"inventory.csv")
date_file = os.path.join(current_directory, r"date.csv")


# Create function to read files
def read_file(file):
    with open(file, newline="") as csvfile:
        # Read the CSV file into a dataframe
        df = pd.read_csv(csvfile)
        # Return the dataframe
        print(df)
