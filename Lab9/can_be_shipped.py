"""CanBeShipped interface-style abstract base class.

A contract for the capability of being shipped. It holds no attributes or
product details, so any kind of object can sign it.
"""

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Implemented by anything that can be physically shipped."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the cost of shipping this item, in dollars."""
