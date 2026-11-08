"""SubscriptionProduct: a Product billed over a recurring period."""

from product import Product
from supplier import Supplier


class SubscriptionProduct(Product):
    """A product with a billing period, which gives access rather than goods."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, billing_months: int) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if billing_months <= 0:
            raise ValueError("Billing period must be greater than zero.")
        self.__billing_months: int = billing_months

    def get_billing_months(self) -> int:
        return self.__billing_months

    def display_information(self) -> None:
        """Print the common product details followed by the billing period."""
        super().display_information()
        print(f"    Billing Period: {self.__billing_months} month(s)")

    def to_dict(self) -> dict[str, object]:
        """Return this product's data, tagged with its type."""
        data = super().to_dict()
        data["type"] = "subscription"
        data["billing_months"] = self.__billing_months
        return data

    def get_fulfilment_info(self) -> str:
        return f"Access is granted and renewed every {self.__billing_months} month(s)."
