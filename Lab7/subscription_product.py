"""SubscriptionProduct: a Product billed over a recurring period."""

from product import Product


class SubscriptionProduct(Product):
    """A product with a billing period, which gives access rather than goods."""

    def __init__(self, product_id, name, price, stock, billing_months):
        super().__init__(product_id, name, price, stock)
        if billing_months <= 0:
            raise ValueError("Billing period must be greater than zero.")
        self.__billing_months = billing_months

    def get_billing_months(self):
        return self.__billing_months

    def display_information(self):
        """Print the common product details followed by the billing period."""
        super().display_information()
        print(f"    Billing Period: {self.__billing_months} month(s)")

    def to_dict(self):
        """Return this product's data, tagged with its type."""
        data = super().to_dict()
        data["type"] = "subscription"
        data["billing_months"] = self.__billing_months
        return data

    def get_fulfilment_info(self):
        return f"Access is granted and renewed every {self.__billing_months} month(s)."
