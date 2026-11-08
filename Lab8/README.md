# INF1103 Lab 8 — Object-Oriented Relationships Part 2

Inventory Management System extended with **association**, **aggregation**,
**composition**, **type hints**, the **Liskov Substitution Principle (LSP)** and
**polymorphism**.

The system still has the Lab 7 product hierarchy (`Product`, `PhysicalProduct`,
`DigitalProduct`, plus the optional `SubscriptionProduct`) and adds `Supplier`,
`Inventory`, `Order` and `OrderLine`.

## Relationship design

| Relationship | Classes | UML notation | Lifecycle decision |
|---|---|---|---|
| Association | `Supplier` 1 — 0..* `Product` | Solid line, no diamond | A supplier is not part of a product. Both exist independently, and `Product` only stores a reference. |
| Aggregation | `Inventory` 0..1 ◇— 0..* `Product` | Hollow diamond at `Inventory` | An inventory groups products but does not create or destroy them. A product can be removed and added to another inventory. |
| Composition | `Order` 1 ◆— 0..* `OrderLine` | Filled diamond at `Order` | `Order` creates its own `OrderLine` objects. A line belongs to one order and is discarded with that order. |
| Association | `OrderLine` 0..* — 1 `Product` | Solid line, no diamond | A line refers to a product but does not own it; the same product can appear in many orders. |
| Generalisation | `Product` ◁— `PhysicalProduct`, `DigitalProduct`, `SubscriptionProduct` | Solid line + hollow triangle | Subclasses are usable anywhere a `Product` is expected (LSP). |
| Realisation | `CanBeShipped` ◁⋯ `PhysicalProduct` | Dashed line + hollow triangle | `PhysicalProduct` implements the shipping capability. |

The full diagram is in [`uml_class_diagram.png`](uml_class_diagram.png).

## Type hints reflect the design

Examples taken from the implementation:

```python
self.supplier: Supplier = supplier                 # association
self.products: list[Product] = []                  # aggregation
self.order_lines: list[OrderLine] = []             # composition

def add_product(self, product: Product) -> None: ...
def find_product(self, product_id: str) -> Product | None: ...
def add_order_line(self, product: Product, quantity: int) -> None: ...
```

`Inventory` stores `Product` references, never `PhysicalProduct` or
`DigitalProduct` collections, so any current or future subclass works without
changing `Inventory`. The `TypeHintTests` in `test_inventory.py` check that the
public domain methods and the `inventory_manager` functions have complete
return and parameter hints.

## Run the project

### Docker (recommended, matches the lab workflow)

```bash
docker build -t inf1103-lab8 .
docker run --rm inf1103-lab8 python -m unittest -v
docker run --rm inf1103-lab8 python demo.py
docker run -it --rm -v "$PWD/inventory.json:/app/inventory.json" inf1103-lab8
```

The last command starts the interactive menu and keeps `inventory.json` on the
host so data survives the container.

### Local Python

Python **3.12+** is required because the code uses `X | None` type hints at
runtime.

```bash
python -m unittest -v
python demo.py
python inventory_manager.py
```

## Files

| File | Purpose |
|---|---|
| `product.py` | Abstract `Product` base class; association to `Supplier` and common behaviour. |
| `physical_product.py` | Shippable product with weight. |
| `digital_product.py` | Product delivered by download. |
| `subscription_product.py` | Optional recurring-access product from Lab 7. |
| `can_be_shipped.py` | Shipping interface-style ABC. |
| `supplier.py` | Independent supplier associated with products. |
| `inventory.py` | Aggregation of `Product` objects. |
| `order.py` | `Order` (whole) and `OrderLine` (part, composition). |
| `inventory_manager.py` | Menu, input validation and JSON persistence. |
| `demo.py` | Demonstration of Sections 2–7 (association, aggregation, composition, LSP, polymorphism). |
| `test_inventory.py` | 15 unit tests covering every Section 9 checklist item. |
| `inventory.json` | Starter data used by the menu program. |
| `Lab8_predict_first_notes.docx` | Predict-first answers, LSP diagnosis, reflection and AI-use note. |
| `uml_class_diagram.png` | Complete UML class diagram with relationships, multiplicities and types. |
| `program_output.txt` | Captured output of `demo.py`. |
| `test_output.txt` | Captured output of the unit tests. |
| `docker_workflow.txt` | Captured Docker build/test/demo commands and output. |
| `docker_build.png` | Docker image build evidence. |
| `docker_images.png` | Built image listed by `docker images`. |
| `docker_run.png` | Tests and demo running inside the container. |
| `docker_app.png` | The interactive menu program running inside the container. |
| `git_workflow.png` | `git status` → `git add` → `git commit` → `git push` → `git log` evidence. |
| `git_log.txt` | Text version of the recent commit history. |

## Submission checklist

- [x] **Predict-first notes** — `Lab8_predict_first_notes.docx` (prediction, what happened, and any change for every Predict First prompt).
- [x] **Python source files** — all modules listed above.
- [x] **Updated UML class diagram** — inheritance, association, aggregation and composition with multiplicities and types (`uml_class_diagram.png`).
- [x] **Evidence of type hints** — hints in every domain class, `inventory_manager.py`, the UML diagram and two dedicated tests.
- [x] **Test code demonstrating the relationships and LSP** — `test_inventory.py` (15 tests, all passing in Docker) and `test_output.txt`.
- [x] **Polymorphic behaviour through `Product` references** — `demo.py` and `program_output.txt`; one loop calls `display_information()` and `get_fulfilment_info()` on mixed product types without `isinstance()` or separate loops.
- [x] **Git and Docker workflow evidence** — `git_workflow.png`, `git_log.txt`, `docker_workflow.txt`, `docker_build.png`, `docker_images.png`, `docker_run.png` and `docker_app.png`.

## Key design notes

- `Supplier` is an **association**, not aggregation: a supplier is not a part of a product, and `Product.supplier` is simply a reference.
- `inventory.remove_product()` only drops the inventory's reference; the product object is unchanged and can be added to another inventory (aggregation).
- `Order.add_order_line()` constructs the `OrderLine` itself, so lines cannot be created elsewhere and passed in (composition).
- `show_product_details(product: Product)` works unchanged for every product subtype; this is polymorphism supported by LSP.
- A subclass that raises `NotImplementedError` for a valid `Product.update_stock()` call would violate LSP. The correct fix is to change the design, not to add subclass checks to `Inventory` (see the diagnosis in the predict-first notes).
