# Imports
from date import read_date
from products import bought_id
from writing_files import write_sold_file, remove_inventory_product
from main import Product


def main():
    ...


# Create class for sold products
class Sold(Product):
    def __init__(self, name, sell_price):
        super().__init__(name)
        self.sell_price = sell_price

    # Add sold products to sold.csv
    def sell(self):
        write_sold_file(
            [
                bought_id(self.name),
                self.name,
                read_date(),
                self.sell_price,
            ]
        )

        # Remove sold product from inventory if present, or subtract count -1
        remove_inventory_product(self.name)


if __name__ == "__main__":
    main()
