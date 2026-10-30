"""Abstract Product class for the Inventory Management System.

Single responsibility: represent and manage what every product has in common.
Every product is a specific type, so Product cannot be instantiated directly;
new product types extend it rather than modifying it (Open-Closed Principle).
"""

from abc import ABC, abstractmethod


class Product(ABC):
    """The common base of every product held in the store's inventory."""

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
        """Print the details shared by every product on one line."""
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self):
        """Return the common data stored in inventory.json for this product."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @abstractmethod
    def get_fulfilment_info(self):
        """Return a message explaining how this product reaches the customer."""
