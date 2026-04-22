from pathlib import Path

import pandas as pd

INPUT_FILE = Path("assets/datasets/Transformed_full/orders_transformed.csv")
OUTPUT_DIR = Path("assets/datasets/Transformed_tables")

CUSTOMERS_FILE = OUTPUT_DIR / "customers.csv"
PRODUCTS_FILE = OUTPUT_DIR / "products.csv"
ORDERS_FILE = OUTPUT_DIR / "orders.csv"


def main() -> None:
    # Read the transformed full dataset
    df = pd.read_csv(INPUT_FILE)

    # Create the customers table
    customers = df[
        ["customer_id", "customer_name", "customer_email", "region"]
    ].drop_duplicates(subset=["customer_id"]).sort_values(by="customer_id")

    # Create the products table
    products = df[
        ["product_id", "product_name", "category", "unit_price"]
    ].drop_duplicates(subset=["product_id"]).sort_values(by="product_id")

    # Create the orders table
    orders = df[
        [
            "order_id",
            "order_timestamp",
            "customer_id",
            "product_id",
            "quantity",
            "payment_method",
            "order_status",
            "order_total",
        ]
    ].drop_duplicates(subset=["order_id"]).sort_values(by="order_timestamp")

    # Ensure output folder exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save tables to CSV
    customers.to_csv(CUSTOMERS_FILE, index=False)
    products.to_csv(PRODUCTS_FILE, index=False)
    orders.to_csv(ORDERS_FILE, index=False)

    print(f"Customers table saved to: {CUSTOMERS_FILE}")
    print(f"Products table saved to: {PRODUCTS_FILE}")
    print(f"Orders table saved to: {ORDERS_FILE}")

    print(f"Customers row count: {len(customers)}")
    print(f"Products row count: {len(products)}")
    print(f"Orders row count: {len(orders)}")


if __name__ == "__main__":
    main()