"""Tests for loading products from a CSV file (Section 5.2)."""

import contextlib
import io
import os
import tempfile
import unittest

from file_loader import load_products
from inventory import Inventory
from supplier import Supplier

HEADER = "product_type,product_id,name,price,stock_quantity\n"
GOOD = ("physical,P001,Desk Lamp,25.00,10\n"
        "digital,D001,Photo Editor,49.90,100\n")
BAD_TYPE = "service,S001,Installation,30.00,5\n"
BAD_PRICE = "physical,P002,Office Chair,abc,3\n"


class LoadProductsTests(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Acme", "a@acme.example")
        self.inventory = Inventory()
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)

    def write(self, name: str, body: str) -> str:
        path = os.path.join(self.directory.name, name)
        with open(path, "w", encoding="utf-8", newline="") as file:
            file.write(HEADER + body)
        return path

    def load(self, path: str) -> str:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            load_products(path, self.inventory, self.supplier)
        return stdout.getvalue()

    def test_valid_rows_are_loaded(self):
        output = self.load(self.write("products.csv", GOOD))
        self.assertEqual(len(self.inventory.products), 2)
        self.assertIn("2 products loaded.", output)
        self.assertIn("Load attempt finished.", output)

    def test_bad_rows_are_skipped_and_the_rest_load(self):
        output = self.load(self.write("products.csv", GOOD + BAD_TYPE + BAD_PRICE
                                      + "physical,P003,Monitor Stand,39.50,7\n"))
        self.assertEqual(len(self.inventory.products), 3)
        self.assertIn("Unknown product type: service", output)
        self.assertIn("Row 5 skipped", output)
        self.assertIn("3 products loaded.", output)

    def test_a_missing_file_is_reported_without_crashing(self):
        output = self.load(os.path.join(self.directory.name, "missing.csv"))
        self.assertEqual(len(self.inventory.products), 0)
        self.assertIn("Products file not found", output)
        self.assertIn("Load attempt finished.", output)
        self.assertNotIn("products loaded.", output)

    def test_a_duplicate_id_is_skipped(self):
        output = self.load(self.write("products.csv", GOOD + GOOD))
        self.assertEqual(len(self.inventory.products), 2)
        self.assertIn("already exists", output)
        self.assertIn("2 products loaded.", output)

    def test_the_finally_message_prints_even_on_a_missing_file(self):
        output = self.load(os.path.join(self.directory.name, "nowhere.csv"))
        self.assertTrue(output.strip().endswith("Load attempt finished."))


if __name__ == "__main__":
    unittest.main()
