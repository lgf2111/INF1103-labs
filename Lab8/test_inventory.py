"""Section 9 checklist tests. Run with: python -m unittest -v"""

import contextlib
import io
import json
import os
import tempfile
import typing
import unittest

import inventory_manager
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order, OrderLine
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier


def make():
    supplier = Supplier("S1", "Acme", "a@acme.example")
    return (supplier,
            PhysicalProduct("P1", "Guitar", 300.0, 5, supplier, 4.0),
            DigitalProduct("D1", "Game", 60.0, 9, supplier, 2048.0),
            SubscriptionProduct("SUB1", "Cloud", 12.0, 3, supplier, 12))


class AssociationTests(unittest.TestCase):
    def test_product_keeps_supplier_after_variable_deleted(self):
        supplier, physical, digital, _ = make()
        del supplier
        self.assertEqual(physical.supplier.name, "Acme")
        self.assertIs(physical.supplier, digital.supplier)
        self.assertIsInstance(physical.supplier, Supplier)


class AggregationTests(unittest.TestCase):
    def test_remove_and_transfer_does_not_destroy_product(self):
        _, physical, _, _ = make()
        a, b = Inventory(), Inventory()
        a.add_product(physical)
        a.remove_product("P1")
        self.assertIsNone(a.find_product("P1"))
        self.assertEqual(physical.get_name(), "Guitar")
        b.add_product(physical)
        self.assertIs(b.find_product("P1"), physical)

    def test_remove_missing_raises(self):
        with self.assertRaises(ValueError):
            Inventory().remove_product("nope")

    def test_duplicate_id_rejected(self):
        _, physical, _, _ = make()
        inv = Inventory()
        inv.add_product(physical)
        with self.assertRaises(ValueError):
            inv.add_product(physical)


class CompositionTests(unittest.TestCase):
    def test_order_creates_lines_and_totals(self):
        _, physical, digital, _ = make()
        order = Order("O1")
        order.add_order_line(physical, 2)
        order.add_order_line(digital, 1)
        self.assertTrue(all(isinstance(l, OrderLine) for l in order.order_lines))
        self.assertAlmostEqual(order.calculate_total(), 660.0)

    def test_same_product_in_two_orders_gives_two_lines_one_product(self):
        _, physical, _, _ = make()
        o1, o2 = Order("O1"), Order("O2")
        o1.add_order_line(physical, 1)
        o2.add_order_line(physical, 1)
        self.assertIsNot(o1.order_lines[0], o2.order_lines[0])
        self.assertIs(o1.order_lines[0].product, o2.order_lines[0].product)

    def test_remove_line_updates_total(self):
        _, physical, digital, _ = make()
        order = Order("O1")
        order.add_order_line(physical, 1)
        order.add_order_line(digital, 1)
        order.remove_order_line("D1")
        self.assertAlmostEqual(order.calculate_total(), 300.0)

    def test_invalid_quantity(self):
        _, physical, _, _ = make()
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(physical, 0)


class TypeHintTests(unittest.TestCase):
    def test_hints_present(self):
        self.assertEqual(typing.get_type_hints(Inventory.find_product)["return"],
                         Product | None)
        self.assertEqual(typing.get_type_hints(Order.add_order_line)["product"], Product)
        self.assertEqual(typing.get_type_hints(OrderLine.calculate_subtotal)["return"], float)
        self.assertEqual(typing.get_type_hints(Product.__init__)["supplier"], Supplier)


class LspPolymorphismTests(unittest.TestCase):
    def test_update_stock_contract_preserved_by_all_subclasses(self):
        for product in make()[1:]:
            product.update_stock(7)
            self.assertEqual(product.get_stock(), 7)
            with self.assertRaises(ValueError):
                product.update_stock(-1)

    def test_one_collection_polymorphic_calls(self):
        supplier, physical, digital, subscription = make()
        inv = Inventory()
        for p in (physical, digital, subscription):
            inv.add_product(p)
        results = [p.get_fulfilment_info() for p in inv.products]
        self.assertIn("physical shipping", results[0])
        self.assertIn("digitally", results[1])
        self.assertIn("renewed", results[2])

    def test_product_is_abstract(self):
        with self.assertRaises(TypeError):
            Product("X", "X", 1.0, 1, make()[0])


class PersistenceTests(unittest.TestCase):
    def test_round_trip_shares_suppliers(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "inventory.json")
            original = inventory_manager.INVENTORY_FILE
            inventory_manager.INVENTORY_FILE = path
            try:
                _, physical, digital, _ = make()
                inv = Inventory()
                inv.add_product(physical)
                inv.add_product(digital)
                inventory_manager.save_inventory(inv)
                with contextlib.redirect_stdout(io.StringIO()):
                    loaded = inventory_manager.load_inventory()
                self.assertEqual(loaded.to_list(), inv.to_list())
                self.assertIs(loaded.find_product("P1").supplier,
                              loaded.find_product("D1").supplier)
            finally:
                inventory_manager.INVENTORY_FILE = original


if __name__ == "__main__":
    unittest.main()
