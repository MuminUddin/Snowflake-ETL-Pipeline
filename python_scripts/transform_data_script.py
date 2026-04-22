from pathlib import Path

import pandas as pd

INPUT_FILE = Path("assets/datasets/Original_file/orders_raw.csv")
OUTPUT_DIR = Path("assets/datasets/Transformed_full")
OUTPUT_FILE = OUTPUT_DIR / "orders_transformed.csv"


def main() -> None:
    # Read the raw CSV into a pandas DataFrame
    df = pd.read_csv(INPUT_FILE)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardise text fields by stripping leading/trailing whitespace
    text_columns = [
        "customer_name",
        "customer_email",
        "region",
        "product_name",
        "category",
        "payment_method",
        "order_status",
    ]

    for col in text_columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Standardise region values so London/london/LONDON all become London
    df["region"] = df["region"].str.title()

    # Fill blank order_status values with Pending
    df["order_status"] = df["order_status"].replace("", "Pending")

    # Convert order_timestamp to datetime
    df["order_timestamp"] = pd.to_datetime(df["order_timestamp"], errors="coerce")

    # Convert quantity to integer and unit_price to float
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Remove rows where key fields failed conversion or are missing
    df = df.dropna(subset=["order_id", "customer_id", "product_id", "order_timestamp", "quantity", "unit_price"])

    # Convert quantity to integer after removing invalid rows
    df["quantity"] = df["quantity"].astype(int)

    # Create derived field: order_total
    df["order_total"] = (df["quantity"] * df["unit_price"]).round(2)

    # Optional cleanup for emails: keep blanks as blanks
    df["customer_email"] = df["customer_email"].replace("nan", "")

    # Sort by timestamp for readability
    df = df.sort_values(by="order_timestamp").reset_index(drop=True)

    # Ensure output folder exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save cleaned data
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Transformed file saved to: {OUTPUT_FILE}")
    print(f"Final row count: {len(df)}")


if __name__ == "__main__":
    main()