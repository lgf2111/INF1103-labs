# Lightweight Python base image
FROM python:3.12-slim

# Working directory inside the container
WORKDIR /app

# Copy the application code into the image
COPY inventory_manager.py .

# Run the inventory manager. inventory.json is expected to live in a mounted
# volume so data persists outside the container even if the container is destroyed.
CMD ["python", "inventory_manager.py"]
