# INF1103 Lab 7: Reflection Task (Optional)

`SubscriptionProduct` was added as a new product type with a billing period in months.

**How well does the current design support adding a new product type?**
Fairly well, but not completely. The product side follows the Open-Closed Principle: the new type is one new class, `subscription_product.py`, which extends `Product`. The main program does not follow it, because it has to know every product type by name.

**Which parts of the existing system needed to change?**

| Part | Changed? |
|---|---|
| `Product`, `PhysicalProduct`, `DigitalProduct` | No |
| `CanBeShipped` | No (a subscription is never shipped, so it does not sign the contract) |
| `Inventory` | No (it only calls methods that every `Product` has) |
| `inventory_manager.py` | Yes, in three places: the import, the `if` chain in `product_from_record()`, and the type menu and `if` chain in `add_product()` |

**How could the design reduce or remove those changes?**
Move the knowledge of product types out of the main program and into a registry (a factory), rather than adding more inheritance. Each product class would provide what the rest of the system needs: its type name, the label of its extra field, and a way to build itself from a saved record. It would register itself in a dictionary that maps type names to classes. `product_from_record()` could then look up `record["type"]`, and `add_product()` could build its menu by looping over the registry. Adding a product type would then mean adding one class and registering it, without changing the code that handles products.
