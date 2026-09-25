"""Persistent order auditor.

Extends the modular auditor with data persistence for a store order system:
- load_inventory() reads previously saved orders from inventory.txt at startup
  (starts with an empty inventory if the file is missing, without error).
- A Python list (array) tracks every valid order entered during the session.
- save_inventory() writes the full order list back to inventory.txt on quit.

Each order is stored as a CSV line: id,product_name,quantity
"""

INVENTORY_FILE = "inventory.txt"
STARTING_ID = 1001


def load_inventory():
    """Load saved orders from the inventory file.

    Returns a list of order dicts: {"id": int, "name": str, "qty": int}.
    If the file does not exist, return an empty list without raising an error.
    """
    orders = []

    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("No existing inventory file found. Starting with an empty inventory.\n")
        return orders

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != 3:
            continue
        order_id, name, qty = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if order_id.isdigit() and qty.lstrip("-").isdigit():
            orders.append({"id": int(order_id), "name": name, "qty": int(qty)})

    return orders


def save_inventory(orders):
    """Save the full order list back to the inventory file."""
    with open(INVENTORY_FILE, "w") as f:
        for order in orders:
            f.write(f"{order['id']},{order['name']},{order['qty']}\n")
    print(f"Order successfully saved to {INVENTORY_FILE}")


def display_orders(orders):
    """Print the current orders in the store."""
    print("Current Orders:\n")
    for order in orders:
        print(f"{order['id']}, {order['name']}, {order['qty']}")
    print()


def next_order_id(orders):
    """Return the next order id, continuing from the highest existing id."""
    if not orders:
        return STARTING_ID
    return max(order["id"] for order in orders) + 1


def get_valid_quantity():
    """Prompt for a quantity and return a positive integer, or None if invalid."""
    raw = input("Enter Quantity: ").strip()
    if not raw or not raw.lstrip("-").isdigit():
        print("Error: Please enter a valid integer quantity.\n")
        return None
    qty = int(raw)
    if qty <= 0:
        print("Error: Quantity must be a positive number.\n")
        return None
    return qty


def main():
    orders = load_inventory()

    while True:
        display_orders(orders)

        name = input("Enter Product Name (or 'quit' to finish): ").strip()
        if name.lower() == "quit":
            save_inventory(orders)
            break
        if not name:
            print("Error: Product name cannot be empty.\n")
            continue

        qty = get_valid_quantity()
        if qty is None:
            continue

        order_id = next_order_id(orders)
        orders.append({"id": order_id, "name": name, "qty": qty})

        print("\nNew Order Added:")
        print(f"{order_id},{name},{qty}\n")


if __name__ == "__main__":
    main()
