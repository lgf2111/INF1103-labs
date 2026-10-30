"""PhysicalProduct: a Product that is stored and shipped."""

from can_be_shipped import CanBeShipped
from product import Product

BASE_SHIPPING_COST = 5.00
SHIPPING_COST_PER_KG = 2.00


class PhysicalProduct(Product, CanBeShipped):
    """A product with a weight, which is a Product and CanBeShipped."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        if weight <= 0:
            raise ValueError("Weight must be greater than zero.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        """Print the common product details followed by the weight."""
        super().display_information()
        print(f"    Weight: {self.__weight:.2f} kg")

    def to_dict(self):
        """Return this product's data, tagged with its type."""
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        """Return a flat base cost plus a charge for each kilogram."""
        return BASE_SHIPPING_COST + SHIPPING_COST_PER_KG * self.__weight
