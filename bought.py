# Imports
from main import Product
from writing_files import write_bought_file, add_inventory_product
from products import bought_id, create_id
from date import read_date


def main():
    ...


# Create child class for bought products
class Bought(Product):
    def __init__(self, name, buy_price, expiration_date):
        super().__init__(name)
        self.buy_price = buy_price
        self.expiration_date = expiration_date

    # Add bought products to bought.csv
    def buy(self):
        write_bought_file(
            [
                create_id(self.name),
                self.name,
                read_date(),
                self.buy_price,
                self.expiration_date,
            ]
        )

        # Add bought product to inventory
        add_inventory_product(
            [
                bought_id(self.name),
                self.name,
                1,
                self.buy_price,
                self.expiration_date,
                read_date(),
            ]
        )


if __name__ == "__main__":
    main()
