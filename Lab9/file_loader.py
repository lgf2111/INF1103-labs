"""Loading products from a CSV file, one bad row at a time.

The file may be missing, a row may name an unknown product type, or a price
may not be a number. Each of those is handled where a useful decision can be
made: the file as a whole, then each row on its own.
"""

import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Read products from a CSV file into the inventory.

    A missing file is reported and the program carries on. A row that cannot
    be turned into a product is reported and skipped, so the valid rows still
    load. "Load attempt finished." always prints.
    """
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            rows = csv.DictReader(file)
            loaded = 0
            for row_number, row in enumerate(rows, start=2):
                try:
                    product = ProductFactory.create(
                        row["product_type"].strip(),
                        row["product_id"].strip(),
                        row["name"].strip(),
                        float(row["price"]),
                        int(row["stock_quantity"]),
                        supplier,
                    )
                    inventory.add_product(product)
                except ValueError as error:
                    print(f"Row {row_number} skipped: {error}")
                    continue
                loaded += 1
            print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
