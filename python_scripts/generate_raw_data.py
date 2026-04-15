import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = Path("assets/datasets/Original_file")
OUTPUT_FILE = OUTPUT_DIR / "orders_raw.csv"

REGIONS = ["London", "london", "LONDON", "Manchester", "Birmingham", "Leeds", "Glasgow"]
CATEGORIES = {
    "Electronics": ["Wireless Mouse", "Bluetooth Speaker", "USB-C Charger", "Webcam"],
    "Home": ["Desk Lamp", "Water Bottle", "Storage Box", "Coffee Mug"],
    "Fashion": ["Hoodie", "T-Shirt", "Trainers", "Backpack"],
    "Books": ["Python Basics", "Data Engineering 101", "Cloud Fundamentals", "SQL for Analytics"],
}
PAYMENT_METHODS = ["Card", "PayPal", "Apple Pay", "Google Pay"]
ORDER_STATUSES = ["Completed", "Pending", "Shipped", "Cancelled", ""]


def random_timestamp(start_days_ago: int = 180) -> str:
    start_date = datetime.now() - timedelta(days=start_days_ago)
    random_seconds = random.randint(0, start_days_ago * 24 * 60 * 60)
    timestamp = start_date + timedelta(seconds=random_seconds)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def build_product_catalog():
    products = []
    for category, names in CATEGORIES.items():
        for name in names:
            products.append(
                {
                    "product_id": f"P{random.randint(1000, 9999)}",
                    "product_name": name,
                    "category": category,
                    "unit_price": round(random.uniform(5.99, 249.99), 2),
                }
            )
    return products


def generate_rows(num_rows: int = 500):
    rows = []
    products = build_product_catalog()

    for _ in range(num_rows):
        product = random.choice(products)

        row = {
            "order_id": f"O{uuid.uuid4().hex[:10].upper()}",
            "order_timestamp": random_timestamp(),
            "customer_id": f"C{random.randint(1000, 9999)}",
            "customer_name": fake.name(),
            "customer_email": fake.email() if random.random() > 0.05 else "",
            "region": random.choice(REGIONS),
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "quantity": random.randint(1, 5),
            "unit_price": f"{product['unit_price']:.2f}",
            "payment_method": random.choice(PAYMENT_METHODS),
            "order_status": random.choice(ORDER_STATUSES),
        }

        rows.append(row)

    if rows:
        rows.append(rows[0].copy())
        rows.append(rows[1].copy())

    return rows


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = generate_rows()

    fieldnames = [
        "order_id",
        "order_timestamp",
        "customer_id",
        "customer_name",
        "customer_email",
        "region",
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "payment_method",
        "order_status",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows at: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()