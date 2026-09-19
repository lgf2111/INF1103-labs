"""Modularized stock delivery auditor."""


def get_valid_input():
    """Prompt for a stock value and return either a valid integer or a quit signal."""
    user_input = input("Enter stock quantity (or 'quit' to finish): ")

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


def generate_report(total_units, failed_attempts):
    """Print a final summary report for the stock audit."""
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    total_units = 0
    failed_attempts = 0
    total_tax = 0.0

    while True:
        user_value = get_valid_input()

        if user_value == "quit":
            generate_report(total_units, failed_attempts)
            break

        if user_value is None:
            failed_attempts += 1
            continue

        total_units = process_delivery(total_units, user_value)
        tax = calculate_tax(user_value)
        total_tax += tax

        print(f"Delivery accepted: {user_value} units. Tax for this delivery: ${tax:.2f}")


if __name__ == "__main__":
    main()
