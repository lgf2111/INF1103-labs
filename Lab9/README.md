# Inventory Management System — Lab 9

INF1103 Programming Fundamentals for Data Engineering, Lab 9: design patterns and
error handling.

This continues the Lab 7/8 Inventory Management System. The product hierarchy,
supplier, inventory, order and order-line model are unchanged. This lab adds:

| Requirement | Where |
|---|---|
| Strategy pattern for order discounts | `discount_strategy.py`, `order.py` |
| Factory pattern for product creation | `product_factory.py` |
| Validation in the class that owns each rule | `product.py`, `order.py`, `discount_strategy.py` |
| Input handling that asks again instead of crashing | `inventory_manager.get_positive_float()` |
| File loading with per-row recovery | `file_loader.load_products()` |
| Automated tests | `tests/` |
| Updated UML class diagram | `uml_class_diagram.png` |
| Predict-first notes | `Lab9_predict_first_notes.docx` |

## Run it

```bash
python3 inventory_manager.py     # menu-driven program, saves to inventory.json
python3 demo.py                  # scripted walkthrough of every new feature
```

Python 3.10 or newer (the code uses `X | None` type hints).

## Test it

```bash
python3 -m unittest discover -s tests -t . -v
```

49 tests covering the Lab 8 model (association, aggregation, composition, LSP,
type hints, persistence) and the Lab 9 work (strategy swapping, factory
creation, validation rules, input retries, CSV recovery).

## The two patterns

**Strategy.** `Order` is given a `DiscountStrategy` and calls `apply()` on it.
It contains no discount branching, so `StudentDiscount` was added without
touching `Order`, and `set_discount()` swaps the behaviour of an existing order.

**Factory.** `ProductFactory.create()` is the only place that names
`PhysicalProduct`, `DigitalProduct` or `SubscriptionProduct`. Menu code, the
JSON loader and the CSV loader all ask the factory. The factory still changes
when a product type is added — that is the Open/Closed issue moved from many
call sites into one method, which is the trade-off the lab asks for.

## Validation and exceptions

- `Product` rejects a price that is not greater than zero and a negative stock.
- `OrderLine` rejects a quantity of zero or less.
- `load_products()` catches `FileNotFoundError` for the file, and `ValueError`
  per row, so a bad row is reported and skipped while the rest load.
  `finally` always prints `Load attempt finished.`
- `get_positive_float()` keeps asking until the user types a number greater than
  zero, handling both a failed `float()` conversion and a failed rule.

## Files

```
discount_strategy.py   DiscountStrategy, NoDiscount, PercentageDiscount,
                       BulkDiscount, StudentDiscount
order.py               Order (uses a strategy) and OrderLine (composition)
product_factory.py     ProductFactory.create()
file_loader.py         load_products(): CSV with per-row error handling
inventory_manager.py   menu, JSON persistence, input helpers
product.py             abstract Product, price and stock rules
physical_product.py    weight, shipping cost, CanBeShipped
digital_product.py     download size
subscription_product.py billing period
supplier.py            Supplier
inventory.py           Inventory (aggregation)
can_be_shipped.py      shipping interface
products.csv           sample file, including two deliberately bad rows
demo.py                scripted demonstration of Sections 2-7
tests/                 unittest suite
uml_class_diagram.png  updated diagram (PlantUML source in .puml)
```

## Docker

```bash
docker build -t inf1103-lab9 .
docker run --rm -it -v "$PWD/inventory.json:/app/inventory.json" inf1103-lab9
docker run --rm inf1103-lab9 python -m unittest discover -s tests -t . -v
```

The image copies the source, the CSV and the tests; `inventory.json` is mounted
so data survives the container.
