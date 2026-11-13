"""Tests for the Strategy pattern: discounts (Section 2)."""

import inspect
import unittest

from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def an_order(total: float = 250.0) -> Order:
    """Return an order whose single line costs `total`."""
    supplier = Supplier("S1", "Acme", "a@acme.example")
    product = ProductFactory.create("digital", "D1", "Bundle", total, 10, supplier)
    order = Order("O1")
    order.add_order_line(product, 1)
    return order


class StrategyTests(unittest.TestCase):
    def test_no_discount_returns_the_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount_takes_a_percentage(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_bulk_discount_applies_at_the_threshold(self):
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(200.0), 180.0)

    def test_bulk_discount_does_nothing_below_the_threshold(self):
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_student_discount_is_five_percent(self):
        self.assertAlmostEqual(StudentDiscount().apply(200.0), 190.0)

    def test_every_strategy_shares_the_same_contract(self):
        for strategy in (NoDiscount(), PercentageDiscount(5), BulkDiscount(200, 20),
                         StudentDiscount()):
            self.assertIsInstance(strategy, DiscountStrategy)
            self.assertTrue(callable(strategy.apply))

    def test_percentage_outside_zero_to_one_hundred_is_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)

    def test_bulk_amount_must_be_smaller_than_the_threshold(self):
        with self.assertRaises(ValueError):
            BulkDiscount(50, 60)


class OrderDiscountTests(unittest.TestCase):
    def test_order_defaults_to_no_discount(self):
        self.assertIsInstance(an_order().discount, NoDiscount)

    def test_order_can_be_created_with_a_strategy(self):
        order = Order("O1", BulkDiscount(200, 20))
        supplier = Supplier("S1", "Acme", "a@acme.example")
        order.add_order_line(
            ProductFactory.create("digital", "D1", "Bundle", 250.0, 1, supplier), 1)
        self.assertAlmostEqual(order.calculate_total(), 230.0)

    def test_set_discount_changes_the_total_of_an_existing_order(self):
        order = an_order(250.0)
        order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_a_new_strategy_needs_no_change_to_order(self):
        class FlatFiveOff(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total - 5

        order = an_order(250.0)
        order.set_discount(FlatFiveOff())
        self.assertAlmostEqual(order.calculate_total(), 245.0)

    def test_order_contains_no_discount_branching(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("if", source)
        self.assertNotIn("discount_type", source)

    def test_two_orders_can_share_one_strategy_object(self):
        shared = PercentageDiscount(10)
        first, second = Order("O1", shared), Order("O2", shared)
        self.assertIs(first.discount, second.discount)

    def test_something_that_is_not_a_strategy_is_rejected(self):
        with self.assertRaises(TypeError):
            Order("O1").set_discount("10 percent")


if __name__ == "__main__":
    unittest.main()
