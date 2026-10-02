"""Inventory Management System with JSON persistence.

Evolves the persistent auditor into a menu-driven CRUD application for a store's
product inventory:
- Products are represented as dictionaries and held in a Python list.
- load_inventory() reads inventory.json at startup if it exists, otherwise it
  begins with an empty inventory (no error raised).
- save_inventory() writes the full inventory back to inventory.json.
- add_product(), update_stock(), search_product() and display_all() provide the
  create / update / read operations over the inventory list.

Each product is stored as a dict: {"id": str, "name": str, "price": float, "stock": int}
"""

import json
import os

INVENTORY_FILE = "inventory.json"

# Default products used only when no inventory.json exists yet.
DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]


def load_inventory():
    """Load the inventory from inventory.json.

    Returns a list of product dicts. If inventory.json exists it is loaded;
    otherwise the function reports this and returns a copy of the default
    starter inventory so the program always has data to work with.
    """
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                inventory = json.load(f)
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("Could not read inventory file. Starting with default inventory.")
            return [dict(product) for product in DEFAULT_INVENTORY]

    print(f"{INVENTORY_FILE} not found. Starting with default inventory.")
    return [dict(product) for product in DEFAULT_INVENTORY]


def save_inventory(inventory):
    """Write the full inventory list back to inventory.json."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)


def find_product(inventory, product_id):
    """Return the product dict matching product_id, or None if not found."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def display_all(inventory):
    """Print every product in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
            )
    print("-" * 48)


def add_product(inventory):
    """Prompt for a new product and append it to the inventory list."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Error: Product ID cannot be empty.")
        return
    if find_product(inventory, product_id):
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

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!")


def update_stock(inventory):
    """Look up a product by ID and set a new stock quantity."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    new_stock = get_valid_stock("\nNew Stock Quantity: ")
    if new_stock is None:
        return

    product["stock"] = new_stock
    print("\nStock updated successfully!")


def search_product(inventory):
    """Look up a product by ID and print its details."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


def get_valid_price(prompt):
    """Prompt for a price and return a non-negative float, or None if invalid."""
    raw = input(prompt).strip()
    try:
        price = float(raw)
    except ValueError:
        print("Error: Please enter a valid price.")
        return None
    if price < 0:
        print("Error: Price cannot be negative.")
        return None
    return price


def get_valid_stock(prompt):
    """Prompt for a stock quantity and return a non-negative int, or None if invalid."""
    raw = input(prompt).strip()
    if not raw or not raw.lstrip("-").isdigit():
        print("Error: Please enter a valid integer quantity.")
        return None
    stock = int(raw)
    if stock < 0:
        print("Error: Stock quantity cannot be negative.")
        return None
    return stock


def print_menu():
    """Print the main menu options."""
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        print_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)
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
