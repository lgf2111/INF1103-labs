"""ProductFactory: the one place that knows how to build a product.

Client code asks the factory for a Product and never imports the concrete
classes, so a new product type is added here rather than at every call site.
"""

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier


class ProductFactory:
    """Builds products by type name and returns them as Product."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, weight: float = 1.0,
               download_size: float = 1.0, billing_months: int = 1) -> Product:
        """Return the Product subclass named by product_type.

        Raises ValueError when the type is unknown or a value is invalid.
        """
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, weight)
        if product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, download_size)
        if product_type == "subscription":
            return SubscriptionProduct(product_id, name, price, stock, supplier,
                                       billing_months)
        raise ValueError(f"Unknown product type: {product_type}")
