"""Discount strategies for the Inventory Management System.

The Strategy pattern: every discount is its own class with the same
apply() method, so Order never needs to know which discount it is using.
Adding a discount means adding a class, not editing Order.
"""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """The shared contract every discount must honour."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the order total after this discount has been applied."""


class NoDiscount(DiscountStrategy):
    """The default: hand the total back unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Take a percentage off the total, e.g. PercentageDiscount(10)."""

    def __init__(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Take a fixed amount off any total at or above a threshold.

    e.g. BulkDiscount(200, 20) takes 20 off a total of 200 or more.
    """

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold <= 0:
            raise ValueError("Threshold must be greater than zero.")
        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")
        if amount >= threshold:
            raise ValueError("Discount amount must be smaller than the threshold.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total


class StudentDiscount(DiscountStrategy):
    """The business's 5% student discount, added without touching Order."""

    def __init__(self, percentage: float = 5.0) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)
