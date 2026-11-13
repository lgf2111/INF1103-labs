"""Demonstrates the Lab 9 work: Strategy, Factory, validation and exceptions."""

from discount_strategy import (BulkDiscount, NoDiscount, PercentageDiscount,
                               StudentDiscount)
from file_loader import load_products
from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


def show_product_details(product: Product) -> None:
    """Works for ANY Product (LSP): no isinstance, no subclass knowledge."""
    product.display_information()
    print("   ->", product.get_fulfilment_info())


def build_250_order(supplier: Supplier) -> Order:
    """An order whose lines add up to exactly 250, for the predict-first check."""
    order = Order("O002")
    course = ProductFactory.create("digital", "D010", "Course Bundle", 125.00, 50,
                                   supplier, download_size=1200.0)
    order.add_order_line(course, 2)
    return order


def main() -> None:
    supplier = Supplier("S001", "TechSource", "sales@techsource.example")

    print("== 2.3 Strategy: one order, three discounts ==")
    order = Order("O001")
    laptop = ProductFactory.create("physical", "P001", "Laptop", 1200.00, 15,
                                   supplier, weight=2.5)
    mouse = ProductFactory.create("physical", "P002", "Mouse", 25.50, 40,
                                  supplier, weight=0.2)
    order.add_order_line(laptop, 1)
    order.add_order_line(mouse, 2)
    print(f"Default (NoDiscount): ${order.calculate_total():.2f}")
    order.set_discount(BulkDiscount(200, 20))
    print(f"BulkDiscount(200, 20): ${order.calculate_total():.2f}")
    order.set_discount(PercentageDiscount(10))
    print(f"PercentageDiscount(10): ${order.calculate_total():.2f}")

    print("\n== 2.4 A fourth strategy, Order unchanged ==")
    order.set_discount(StudentDiscount())
    print(f"StudentDiscount(5%): ${order.calculate_total():.2f}")

    print("\n== Predict first: a 250 order ==")
    cart = build_250_order(supplier)
    print(f"Subtotal: ${sum(l.calculate_subtotal() for l in cart.order_lines):.2f}")
    cart.set_discount(BulkDiscount(200, 20))
    print(f"BulkDiscount(200, 20): ${cart.calculate_total():.2f}")
    cart.set_discount(PercentageDiscount(10))
    print(f"then PercentageDiscount(10): ${cart.calculate_total():.2f}")

    print("\n== 3.2 An unknown product type ==")
    try:
        ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
    except ValueError as error:
        print(f"Caught ValueError: {error}")

    print("\n== 4. Validation belongs to the class that owns the rule ==")
    for description, action in (
            ("price of 0", lambda: ProductFactory.create("physical", "P010", "Bad", 0, 1,
                                                         supplier)),
            ("negative stock", lambda: ProductFactory.create("physical", "P011", "Bad", 5.0,
                                                             -1, supplier)),
            ("quantity of 0", lambda: Order("O003").add_order_line(laptop, 0))):
        try:
            action()
        except ValueError as error:
            print(f"{description}: {error}")

    print("\n== 5.2 Loading products.csv ==")
    inventory = Inventory()
    load_products("products.csv", inventory, supplier)
    inventory.display_all()

    print("\n== 5.2 A file that is not there ==")
    load_products("products-not-here.csv", inventory, supplier)

    print("\n== 7. Polymorphism through the common Product type ==")
    for product in inventory.products:
        show_product_details(product)

    print("\nDefault discount object:", type(NoDiscount()).__name__)


if __name__ == "__main__":
    main()
