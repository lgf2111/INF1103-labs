"""Inventory class for the Inventory Management System.

Single responsibility: manage a collection of Product objects.
"""


class Inventory:
    """The collection of products held by the store."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Store a product, rejecting an ID that is already in use."""
        if self.search_product(product.get_product_id()) is not None:
            raise ValueError("A product with that ID already exists.")
        self.__products.append(product)

    def search_product(self, product_id):
        """Return the Product matching product_id, or None if not found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        """Print every product in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 48)

    def to_list(self):
        """Return every product's data in the form stored in inventory.json."""
        return [product.to_dict() for product in self.__products]
