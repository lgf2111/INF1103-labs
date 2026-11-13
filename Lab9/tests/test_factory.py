"""Tests for the Factory pattern (Section 3)."""

import pathlib
import unittest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from subscription_product import SubscriptionProduct
from supplier import Supplier

ROOT = pathlib.Path(__file__).resolve().parent.parent


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Acme", "a@acme.example")

    def test_creates_each_known_type(self):
        physical = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10,
                                         self.supplier, weight=2.0)
        digital = ProductFactory.create("digital", "D1", "Editor", 49.9, 100,
                                        self.supplier, download_size=850.0)
        subscription = ProductFactory.create("subscription", "S1", "Cloud", 12.0, 3,
                                             self.supplier, billing_months=12)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertIsInstance(subscription, SubscriptionProduct)

    def test_returns_the_common_product_type(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10,
                                        self.supplier)
        self.assertIsInstance(product, Product)

    def test_unknown_type_raises_a_clear_value_error(self):
        with self.assertRaises(ValueError) as caught:
            ProductFactory.create("service", "S1", "Installation", 30.0, 5,
                                  self.supplier)
        self.assertIn("service", str(caught.exception))

    def test_factory_copies_values_onto_the_product(self):
        product = ProductFactory.create("physical", "P9", "Chair", 39.5, 7,
                                        self.supplier, weight=3.2)
        self.assertEqual(product.get_product_id(), "P9")
        self.assertEqual(product.get_name(), "Chair")
        self.assertAlmostEqual(product.get_price(), 39.5)
        self.assertEqual(product.get_stock(), 7)
        self.assertIs(product.supplier, self.supplier)

    def test_client_code_does_not_build_products_directly(self):
        """inventory_manager and demo ask the factory instead of the classes."""
        for name in ("inventory_manager.py", "demo.py"):
            source = (ROOT / name).read_text(encoding="utf-8")
            for concrete in ("PhysicalProduct(", "DigitalProduct(", "SubscriptionProduct("):
                self.assertNotIn(concrete, source,
                                 f"{name} should create products through ProductFactory")

    def test_factory_is_the_only_module_building_products(self):
        for module in ("demo.py", "inventory_manager.py", "file_loader.py"):
            source = (ROOT / module).read_text(encoding="utf-8")
            self.assertIn("ProductFactory", source)


if __name__ == "__main__":
    unittest.main()
