"""Abstract Product class for the Inventory Management System.

Single responsibility: represent and manage what every product has in common.
Every product is a specific type, so Product cannot be instantiated directly;
new product types extend it rather than modifying it (Open-Closed Principle).
"""

from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    """The common base of every product held in the store's inventory."""

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = 0
        self.supplier: Supplier = supplier  # association
        self.update_stock(stock)

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        """Set the stock level, rejecting a negative quantity."""
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        """Print the details shared by every product on one line."""
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self) -> dict[str, object]:
        """Return the common data stored in inventory.json for this product."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.to_dict(),
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message explaining how this product reaches the customer."""
