"""Demonstrates the Lab 8 relationships, LSP and polymorphism (Sections 2-7)."""

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> None:
    """Works for ANY Product (LSP): no isinstance, no subclass knowledge."""
    product.display_information()
    print("   ->", product.get_fulfilment_info())


def main() -> None:
    print("== 2. Association: Supplier - Product ==")
    supplier = Supplier("S001", "TechSource", "sales@techsource.example")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
    antivirus = DigitalProduct("D001", "Antivirus", 39.90, 100, supplier, 850.0)
    del supplier  # the products still hold their own references
    laptop.supplier.display_information()
    antivirus.supplier.display_information()
    print("Same Supplier object:", laptop.supplier is antivirus.supplier)

    print("\n== 3. Aggregation: Inventory - Product ==")
    inv_a, inv_b = Inventory(), Inventory()
    inv_a.add_product(laptop)
    inv_a.remove_product("P001")
    print("Laptop still usable after removal:", laptop.get_name(), laptop.get_stock())
    inv_b.add_product(laptop)
    inv_b.add_product(antivirus)
    print("Laptop in A:", inv_a.find_product("P001"), "| in B:",
          inv_b.find_product("P001") is laptop)

    print("\n== 4. Composition: Order - OrderLine ==")
    order1, order2 = Order("O001"), Order("O002")
    order1.add_order_line(laptop, 2)
    order1.add_order_line(antivirus, 1)
    order2.add_order_line(laptop, 1)
    order1.display()
    order2.display()
    print("OrderLine objects distinct:",
          order1.order_lines[0] is not order2.order_lines[0])
    print("Product object shared:",
          order1.order_lines[0].product is order2.order_lines[0].product)
    order1.remove_order_line("D001")
    print("After removing a line, order 1 total: $%.2f" % order1.calculate_total())

    print("\n== 6/7. LSP and polymorphism ==")
    for product in inv_b.products:
        show_product_details(product)


if __name__ == "__main__":
    main()
