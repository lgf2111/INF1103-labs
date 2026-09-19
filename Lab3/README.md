# Lab 3: Modular Auditor

## Function signatures

```python
def get_valid_input(): ...
def process_delivery(current_total, new_value): ...
def calculate_tax(amount): ...
def generate_report(total_units, failed_attempts): ...
```

- `get_valid_input()` prompts for a delivery, rejects invalid or negative
  values, and returns a valid integer, `"quit"`, or `None` for a rejected
  entry.
- `process_delivery(current_total, new_value)` returns the updated inventory
  total.
- `calculate_tax(amount)` returns 10% of the delivery amount.
- `generate_report(total_units, failed_attempts)` prints the final summary.

## Run locally

```bash
python3 modular_auditor.py
```

## Run with a Docker volume mount

From the repository root:

```bash
docker build -t modular-auditor ./Lab3
docker run --rm -it -v "$(pwd)/Lab3:/app" modular-auditor
```

The volume mount makes the local Lab 3 files available in the container while
the program runs interactively.

## Self-reflection

`calculate_tax()` returns a value instead of printing it so that the caller can
decide what to do with the result. The tax can later be added to a report,
written to a file, or sent to another system without changing the calculation
function. Keeping calculation separate from output makes the function easier to
reuse and test.
