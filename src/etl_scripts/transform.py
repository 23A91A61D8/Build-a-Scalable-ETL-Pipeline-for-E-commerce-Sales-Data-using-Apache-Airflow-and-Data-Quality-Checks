import pandas as pd
import logging
import hashlib


def transform_sales_data(raw_path: str, transformed_path: str) -> None:
    """
    Cleans and enriches raw e-commerce sales data
    and saves the transformed data.
    """

    try:
        logging.info("Starting data transformation")

        # Read raw data
        df = pd.read_csv(raw_path)

        # Drop rows with critical missing values
        df.dropna(subset=["InvoiceNo", "StockCode"], inplace=True)

        # Fill missing numeric values
        df["Quantity"] = df["Quantity"].fillna(0).astype(int)
        df["UnitPrice"] = df["UnitPrice"].fillna(0).astype(float)

        # Remove duplicate records
        df.drop_duplicates(subset=["InvoiceNo", "StockCode"], inplace=True)

        # Create derived column
        df["total_item_price"] = df["Quantity"] * df["UnitPrice"]

        # Generate customer_id if missing or non-unique
        df["CustomerID"] = df["CustomerID"].fillna("UNKNOWN").astype(str)
        df["customer_id"] = df["CustomerID"].apply(
            lambda x: hashlib.md5(x.encode()).hexdigest()
        )

        # Convert InvoiceDate to datetime
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

        # Save transformed data
        df.to_csv(transformed_path, index=False)

        logging.info(f"Data successfully transformed and saved to {transformed_path}")

    except Exception as e:
        logging.error("Error during data transformation")
        raise e
