def get_valid_input():
    """Prompt for a non-negative delivery quantity or the quit signal."""
    user_input = input("Enter stock quantity (or 'quit' to finish): ").strip()

    if user_input.lower() == "quit":
        return "quit"

    try:
        delivery_amount = int(user_input)
    except ValueError:
        print("Error: Please enter a valid integer or 'quit'.")
        return None

    if delivery_amount < 0:
        print("Error: Negative stock quantity is not allowed.")
        return None

    return delivery_amount


def process_delivery(current_total, new_value):
    """Add one valid delivery to the running total."""
    return current_total + new_value


def calculate_tax(amount):
    """Return 10% tax for one delivery."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Print the final audit summary."""
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    inventory = 0
    failed_entries = 0
    total_tax = 0

    while True:
        delivery = get_valid_input()

        if delivery == "quit":
            generate_report(inventory, failed_entries)
            break

        if delivery is None:
            failed_entries += 1
            continue

        inventory = process_delivery(inventory, delivery)
        total_tax += calculate_tax(delivery)


if __name__ == "__main__":
    main()
