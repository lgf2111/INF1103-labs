"""Persistent stock delivery auditor.

Extends the modular auditor with data persistence:
- load_inventory() reads the previously saved total and transaction history
  from inventory.txt at startup (starts empty if the file is missing).
- A Python list tracks every valid transaction amount entered.
- save_inventory() writes the final total and transaction history back to
  inventory.txt when the user quits.
"""

INVENTORY_FILE = "inventory.txt"


def load_inventory():
    """Load the saved total and transaction history from the inventory file.

    Returns a tuple of (total_units, history_list). If the file does not
    exist, start with a total of 0 and an empty history list without error.
    """
    total_units = 0
    history = []

    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("No existing inventory file found. Starting with an empty inventory.")
        return total_units, history

    for line in lines:
        if not line:
            continue
        if line.startswith("TOTAL:"):
            try:
                total_units = int(line.split(":", 1)[1].strip())
            except ValueError:
                total_units = 0
        elif line.startswith("HISTORY:"):
            values = line.split(":", 1)[1].strip()
            if values:
                for item in values.split(","):
                    item = item.strip()
                    if item.lstrip("-").isdigit():
                        history.append(int(item))

    return total_units, history


def save_inventory(total_units, history):
    """Save the final total and transaction history list to the inventory file."""
    with open(INVENTORY_FILE, "w") as f:
        f.write(f"TOTAL: {total_units}\n")
        history_str = ",".join(str(value) for value in history)
        f.write(f"HISTORY: {history_str}\n")
    print(f"Inventory successfully saved to {INVENTORY_FILE}")


def get_valid_input():
    """Prompt for a stock value and return either a valid integer or a quit signal."""
    try:
        user_input = input("Enter stock quantity (or 'quit' to finish): ")
    except EOFError:
        print("\nInput closed. Ending audit.")
        return "quit"

    if user_input.strip().lower() == "quit":
        return "quit"

    if not user_input.strip() or not user_input.strip().lstrip("-").isdigit():
        print("Error: Please enter a valid integer or 'quit'.")
        return None

    value = int(user_input.strip())

    if value < 0:
        print("Error: Negative stock quantity is not allowed.")
        return None

    return value


def process_delivery(current_total, new_value):
    """Add a valid delivery value to the running total and return the new total."""
    return current_total + new_value


def calculate_tax(amount):
    """Return tax for a delivery value using a 10% rate."""
    return amount * 0.10


def generate_report(total_units, failed_attempts, history):
    """Print a final summary report for the stock audit."""
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {history}")


def main():
    total_units, history = load_inventory()
    failed_attempts = 0
    total_tax = 0.0

    print("Current Inventory:")
    print(f"Starting Total: {total_units}")
    print(f"Transaction History: {history}\n")

    while True:
        user_value = get_valid_input()

        if user_value == "quit":
            generate_report(total_units, failed_attempts, history)
            save_inventory(total_units, history)
            break

        if user_value is None:
            failed_attempts += 1
            continue

        total_units = process_delivery(total_units, user_value)
        history.append(user_value)
        tax = calculate_tax(user_value)
        total_tax += tax

        print(f"Delivery accepted: {user_value} units. Tax for this delivery: ${tax:.2f}")


if __name__ == "__main__":
    main()
