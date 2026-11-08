"""DigitalProduct: a Product delivered through a download."""

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product with a download size, which never needs shipping."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size <= 0:
            raise ValueError("Download size must be greater than zero.")
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        """Print the common product details followed by the download size."""
        super().display_information()
        print(f"    Download Size: {self.__download_size:.2f} MB")

    def to_dict(self) -> dict[str, object]:
        """Return this product's data, tagged with its type."""
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."
