# INF1103 Lab 6: Reflection Questions

**1. What is the difference between a class and an object?**
A class is the blueprint that defines which attributes and methods something has. An object is one instance created from that blueprint with its own values. `Product` is a class; `Product("P001", "Laptop", 1200.00, 15)` creates an object.

**2. Why is Product a suitable class for this system?**
A product is a real thing in the system's description, with its own data (ID, name, price, stock) and its own behaviour (updating stock, displaying itself). In Week 5 that data sat in dictionaries while the functions acting on it sat elsewhere. A class keeps the two together.

**3. What data belongs inside a Product object?**
The product ID, name, price and stock quantity, because they describe that one product. Data about other products or the application, such as the file name or the product list, does not belong there.

**4. Why should the Product class manage its own stock rather than the main program directly changing it?**
All changes then go through `update_stock()`, so the rule that stock cannot be negative is enforced in one place. Any code that changes stock gets that rule automatically, and the rule only needs to change in one place.

**5. What does encapsulation mean in your program?**
`Product` and `Inventory` keep their attributes private (`__stock`, `__products`) and other code uses their public methods, such as `update_stock()`, `get_name()` and `search_product()`. Python only applies name mangling rather than strictly enforcing this, but the double underscore makes the intent clear.

**6. What is the responsibility of the Product class?**
To represent and manage one product: storing its data, protecting its stock value and displaying its information.

**7. What is the responsibility of the Inventory class?**
To manage a collection of `Product` objects: storing them, adding them while rejecting duplicate IDs, searching them and displaying them all.

**8. How does separating these responsibilities demonstrate the Single Responsibility Principle?**
Each part has one reason to change. A new rule about stock changes `Product`, a change to how products are stored or found changes `Inventory`, and a change to the menu or the file format changes only the main program.

**9. What information does the main program need to know about a Product?**
Only its public interface: how to create one, and the methods it calls (`get_name()`, `get_stock()`, `update_stock()`, `display_information()`, `to_dict()`).

**10. What information about the internal implementation of Product does the main program not need to know?**
How the attributes are stored and named, how stock is validated, and how the display line is formatted. Any of these could change without changing the main program, as long as the public methods stay the same.
