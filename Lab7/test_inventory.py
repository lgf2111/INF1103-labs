"""Tests for the Section 7 checklist. Run with: python -m unittest -v"""

import contextlib
import io
import json
import os
import tempfile
import unittest

import inventory_manager
from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct


def displayed(product):
    """Return what product.display_information() prints."""
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        product.display_information()
    return output.getvalue()


class ProductTypeTests(unittest.TestCase):
    def setUp(self):
        self.physical = PhysicalProduct("P001", "Guitar", 300.00, 5, 4.0)
        self.digital = DigitalProduct("D001", "Operating System", 150.00, 99, 4096.0)

    def test_physical_displays_common_information_and_weight(self):
        output = displayed(self.physical)
        self.assertIn("ID: P001 | Name: Guitar | Price: $300.00 | Stock: 5", output)
        self.assertIn("Weight: 4.00 kg", output)

    def test_digital_displays_common_information_and_download_size(self):
        output = displayed(self.digital)
        self.assertIn("ID: D001 | Name: Operating System", output)
        self.assertIn("Download Size: 4096.00 MB", output)

    def test_both_subclasses_implement_fulfilment(self):
        self.assertIn("physical shipping", self.physical.get_fulfilment_info())
        self.assertIn("digitally", self.digital.get_fulfilment_info())

    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("P001", "Generic", 1.00, 1)

    def test_shipping_cost_depends_on_weight(self):
        light = PhysicalProduct("P002", "Mouse", 25.50, 40, 0.5)
        self.assertEqual(light.calculate_shipping_cost(), 6.00)
        self.assertEqual(self.physical.calculate_shipping_cost(), 13.00)

    def test_only_physical_products_can_be_shipped(self):
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))

    def test_physical_product_has_one_parent_class(self):
        self.assertFalse(issubclass(CanBeShipped, Product))
        self.assertTrue(issubclass(PhysicalProduct, Product))

    def test_invalid_values_are_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P003", "Bad", 1.00, 1, 0)
        with self.assertRaises(ValueError):
            DigitalProduct("D002", "Bad", 1.00, 1, -1)
        with self.assertRaises(ValueError):
            self.physical.update_stock(-1)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.product = PhysicalProduct("P001", "Guitar", 300.00, 5, 4.0)
        self.inventory.add_product(self.product)

    def test_search_finds_and_misses(self):
        self.assertIs(self.inventory.search_product("P001"), self.product)
        self.assertIsNone(self.inventory.search_product("P999"))

    def test_duplicate_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.add_product(DigitalProduct("P001", "Other", 1.00, 1, 1.0))

    def test_update_stock_through_search(self):
        self.inventory.search_product("P001").update_stock(50)
        self.assertEqual(self.product.get_stock(), 50)


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = os.path.join(directory.name, "inventory.json")
        original = inventory_manager.INVENTORY_FILE
        inventory_manager.INVENTORY_FILE = self.path
        self.addCleanup(setattr, inventory_manager, "INVENTORY_FILE", original)

    def load(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return inventory_manager.load_inventory()

    def test_save_and_load_preserve_types_and_attributes(self):
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P001", "Guitar", 300.00, 5, 4.0))
        inventory.add_product(DigitalProduct("D001", "Game", 60.00, 9, 2048.0))
        inventory.add_product(SubscriptionProduct("S001", "Cloud", 12.00, 100, 12))
        inventory_manager.save_inventory(inventory)

        loaded = self.load()
        physical = loaded.search_product("P001")
        digital = loaded.search_product("D001")
        subscription = loaded.search_product("S001")

        self.assertIsInstance(physical, PhysicalProduct)
        self.assertEqual(physical.get_weight(), 4.0)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(digital.get_download_size(), 2048.0)
        self.assertIsInstance(subscription, SubscriptionProduct)
        self.assertEqual(subscription.get_billing_months(), 12)
        self.assertEqual(loaded.to_list(), inventory.to_list())

    def test_saved_records_contain_a_type_identifier(self):
        inventory_manager.save_inventory(self.load())
        with open(self.path) as f:
            types = {record["type"] for record in json.load(f)}
        self.assertEqual(types, {"physical", "digital"})

    def test_unknown_type_falls_back_to_default_inventory(self):
        with open(self.path, "w") as f:
            json.dump([{"id": "X", "name": "X", "price": 1, "stock": 1, "type": "?"}], f)
        self.assertIsNotNone(self.load().search_product("P001"))


if __name__ == "__main__":
    unittest.main()
