"""Inventory class: aggregation. It groups Products but does not own them."""

from product import Product


class Inventory:
    """The collection of products held by the store."""

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Store a reference to an existing product, rejecting a duplicate ID."""
        if self.find_product(product.get_product_id()) is not None:
            raise ValueError("A product with that ID already exists.")
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        """Drop the reference only; the Product itself is not destroyed."""
        product = self.find_product(product_id)
        if product is None:
            raise ValueError("No product with that ID.")
        self.products.remove(product)

    def find_product(self, product_id: str) -> Product | None:
        """Return the matching Product, or None if it cannot be found."""
        for product in self.products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        """Print every product, whatever its subclass (polymorphism / LSP)."""
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.products:
            print("No products in inventory.")
        else:
            for product in self.products:
                product.display_information()
        print("-" * 48)

    def to_list(self) -> list[dict[str, object]]:
        return [product.to_dict() for product in self.products]
