"""Tests for validation and input handling (Sections 4 and 5.1)."""

import contextlib
import io
import unittest
from unittest.mock import patch

import inventory_manager
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Acme", "a@acme.example")

    def test_a_price_of_zero_is_rejected(self):
        with self.assertRaises(ValueError) as caught:
            ProductFactory.create("physical", "P1", "Lamp", 0, 10, self.supplier)
        self.assertIn("price", str(caught.exception).lower())

    def test_a_negative_price_is_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", -5, 10, self.supplier)

    def test_negative_stock_is_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", 25.0, -1, self.supplier)

    def test_a_quantity_of_zero_is_rejected(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier)
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(product, 0)

    def test_a_subclass_cannot_relax_a_rule_from_product(self):
        """LSP: the stock rule is part of Product's contract, so every type keeps it."""
        for product_type in ("physical", "digital", "subscription"):
            product = ProductFactory.create(product_type, "X1", "Item", 10.0, 1,
                                            self.supplier)
            with self.assertRaises(ValueError):
                product.update_stock(-1)


class PositiveFloatTests(unittest.TestCase):
    def run_with_inputs(self, *values):
        stdout = io.StringIO()
        with patch("builtins.input", side_effect=list(values)), \
                contextlib.redirect_stdout(stdout):
            result = inventory_manager.get_positive_float("Price: ")
        return result, stdout.getvalue()

    def test_text_is_rejected_then_zero_then_a_valid_number(self):
        result, output = self.run_with_inputs("abc", "0", "12.50")
        self.assertAlmostEqual(result, 12.5)
        self.assertIn("Please enter a valid number, e.g. 12.50", output)
        self.assertIn("Please enter a number greater than zero.", output)

    def test_a_negative_number_is_rejected(self):
        result, output = self.run_with_inputs("-5", "8")
        self.assertAlmostEqual(result, 8.0)
        self.assertIn("greater than zero", output)

    def test_the_first_valid_number_is_returned_immediately(self):
        result, output = self.run_with_inputs("3.25")
        self.assertAlmostEqual(result, 3.25)
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()
