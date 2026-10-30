"""Product class for the Inventory Management System.

Single responsibility: represent and manage one product. It does not read
user input, touch inventory.json, or know about the rest of the inventory.
"""


class Product:
    """A single product held in the store's inventory."""

    def __init__(self, product_id, name, price, stock):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = 0
        self.update_stock(stock)

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Set the stock level, rejecting a negative quantity."""
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        """Print this product's details on one line."""
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self):
        """Return this product's data in the form stored in inventory.json."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
