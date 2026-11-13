"""Order and OrderLine: composition. An Order creates and owns its lines.

The order no longer decides discounts itself. It is given a DiscountStrategy
and only calls apply(), so a new discount never changes this class.
"""

from discount_strategy import DiscountStrategy, NoDiscount
from product import Product


class OrderLine:
    """One product and quantity inside one Order. Only Order should create it."""

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product  # association: the line does not own it
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity

    def display(self) -> None:
        print(f"  {self.quantity} x {self.product.get_name()} "
              f"@ ${self.product.get_price():.2f} = ${self.calculate_subtotal():.2f}")


class Order:
    """Whole in the composition: creates, manages and removes its OrderLines.

    It uses a DiscountStrategy (association): the strategy is passed in, is
    never created here, and can be shared between orders.
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Replace the discount without changing anything else about the order."""
        if not isinstance(discount, DiscountStrategy):
            raise TypeError("Discount must be a DiscountStrategy.")
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create the OrderLine internally (never accept one from outside)."""
        self.order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> None:
        """Remove the line for a product; the line is discarded with the order."""
        self.order_lines = [l for l in self.order_lines
                            if l.product.get_product_id() != product_id]

    def calculate_total(self) -> float:
        """Subtotal the lines, then let the strategy decide the final total."""
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display(self) -> None:
        print(f"Order {self.order_id}")
        for line in self.order_lines:
            line.display()
        subtotal = sum(line.calculate_subtotal() for line in self.order_lines)
        total = self.calculate_total()
        print(f"  Subtotal: ${subtotal:.2f}")
        if total != subtotal:
            print(f"  Discount ({type(self.discount).__name__}): -${subtotal - total:.2f}")
        print(f"  Total: ${total:.2f}")
