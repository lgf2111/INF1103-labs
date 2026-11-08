"""Inventory Management System for Lab 8.

Extends the Lab 7 product hierarchy with Supplier, Inventory, Order and OrderLine,
demonstrating association, aggregation, composition, type hints, LSP and
polymorphism. This main program is responsible for:
- Displaying the menu and getting user input.
- Calling the appropriate Inventory and Product methods.
- Loading inventory.json at startup and saving it back (file handling), using
  each record's "type" to rebuild the correct Product subclass.
"""

import json
import math
import os

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier

INVENTORY_FILE = "inventory.json"


def create_default_inventory() -> Inventory:
    """Return an Inventory holding the starter products."""
    inventory = Inventory()
    tech = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
    soft = Supplier("S002", "SoftWorks", "hello@softworks.example")
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, tech, 2.5))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, tech, 0.2))
    inventory.add_product(PhysicalProduct("P003", "Keyboard", 45.00, 25, tech, 0.8))
    inventory.add_product(DigitalProduct("D001", "Antivirus", 39.90, 100, soft, 850.0))
    return inventory


def supplier_from_record(record: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """Return the shared Supplier for a record, creating it the first time."""
    data = record["supplier"]
    if data["supplier_id"] not in suppliers:
        suppliers[data["supplier_id"]] = Supplier(
            data["supplier_id"], data["name"], data["contact_email"])
    return suppliers[data["supplier_id"]]


def product_from_record(record: dict, suppliers: dict[str, Supplier]) -> Product:
    """Create the Product subclass named by a saved record's "type"."""
    common = (record["id"], record["name"], record["price"], record["stock"],
              supplier_from_record(record, suppliers))
    product_type = record["type"]
    if product_type == "physical":
        return PhysicalProduct(*common, record["weight"])
    if product_type == "digital":
        return DigitalProduct(*common, record["download_size"])
    if product_type == "subscription":
        return SubscriptionProduct(*common, record["billing_months"])
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory() -> Inventory:
    """Build an Inventory from inventory.json.

    If the file is missing or unreadable, the function reports this and
    returns the default starter inventory so the program always has data.
    """
    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with default inventory.")
        return create_default_inventory()

    print(f"{INVENTORY_FILE} found.")
    try:
        with open(INVENTORY_FILE, "r") as f:
            records = json.load(f)
        inventory = Inventory()
        suppliers = {}
        for record in records:
            inventory.add_product(product_from_record(record, suppliers))
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        print("Could not read inventory file. Starting with default inventory.")
        return create_default_inventory()

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory) -> None:
    """Write the full inventory back to inventory.json."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory.to_list(), f, indent=4)


def add_product(inventory: Inventory) -> None:
    """Prompt for a new product and add it to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Error: Product ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:
        print("Error: A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Error: Product name cannot be empty.")
        return

    price = get_valid_price("Price: ")
    if price is None:
        return

    stock = get_valid_stock("Stock Quantity: ")
    if stock is None:
        return

    print("\nSupplier")
    supplier_id = input("Supplier ID: ").strip()
    known = next((p.supplier for p in inventory.products
                  if p.supplier.supplier_id == supplier_id), None)
    if known is not None:
        supplier = known
    else:
        supplier_name = input("Supplier Name: ").strip()
        email = input("Supplier Email: ").strip()
        if not supplier_id or not supplier_name:
            print("Error: Supplier ID and name cannot be empty.")
            return
        supplier = Supplier(supplier_id, supplier_name, email)

    print("\nProduct Type")
    print("1. Physical")
    print("2. Digital")
    print("3. Subscription")
    product_type = input("Enter type: ").strip()

    if product_type == "1":
        weight = get_valid_size("Weight (kg): ")
        if weight is None:
            return
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    elif product_type == "2":
        download_size = get_valid_size("Download Size (MB): ")
        if download_size is None:
            return
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
    elif product_type == "3":
        billing_months = get_valid_stock("Billing Period (months): ")
        if billing_months is None:
            return
        if billing_months == 0:
            print("Error: Billing period must be greater than zero.")
            return
        product = SubscriptionProduct(product_id, name, price, stock, supplier, billing_months)
    else:
        print("Error: Please choose a product type from 1-3.")
        return

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    """Look up a product by ID and set a new stock quantity."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    new_stock = get_valid_stock("\nNew Stock Quantity: ")
    if new_stock is None:
        return

    product.update_stock(new_stock)
    print("\nStock updated successfully!")


def search_product(inventory: Inventory) -> None:
    """Look up a product by ID and print its details."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print(f"Supplier: {product.supplier.name} ({product.supplier.contact_email})")
    print("-" * 48)


def get_valid_price(prompt: str) -> float | None:
    """Prompt for a price and return a non-negative float, or None if invalid."""
    raw = input(prompt).strip()
    try:
        price = float(raw)
    except ValueError:
        print("Error: Please enter a valid price.")
        return None
    if not math.isfinite(price):
        print("Error: Please enter a valid price.")
        return None
    if price < 0:
        print("Error: Price cannot be negative.")
        return None
    return price


def get_valid_size(prompt: str) -> float | None:
    """Prompt for a weight or download size and return a positive float, or None."""
    raw = input(prompt).strip()
    try:
        size = float(raw)
    except ValueError:
        print("Error: Please enter a valid number.")
        return None
    if not math.isfinite(size) or size <= 0:
        print("Error: Please enter a number greater than zero.")
        return None
    return size


def get_valid_stock(prompt: str) -> int | None:
    """Prompt for a stock quantity and return a non-negative int, or None if invalid."""
    raw = input(prompt).strip()
    try:
        stock = int(raw)
    except ValueError:
        print("Error: Please enter a valid integer quantity.")
        return None
    if stock < 0:
        print("Error: Stock quantity cannot be negative.")
        return None
    return stock


def print_menu() -> None:
    """Print the main menu options."""
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        print_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
