inventory = 0
failed_entries = 0

while True:
    user_input = input("Enter stock quantity (or 'quit' to finish): ")

    if user_input.lower() == "quit":
        print(f"Total Units Processed: {inventory}")
        print(f"Number of Failed/Rejected Entries: {failed_entries}")
        break

    if not user_input.isdigit():
        print("Error: Please enter a valid integer or 'quit'.")
        failed_entries += 1
        continue

    stock = int(user_input)

    if stock < 0:
        print("Error: Negative stock quantity is not allowed.")
        failed_entries += 1
        continue

    inventory += stock

    if inventory > 500:
        print("Alert: Inventory exceeds 500 units!")
        break
