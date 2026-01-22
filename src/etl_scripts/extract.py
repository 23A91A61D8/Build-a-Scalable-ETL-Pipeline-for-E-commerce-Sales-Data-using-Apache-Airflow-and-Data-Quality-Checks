import os
import logging
import pandas as pd


def extract_sales_data(source_path: str, output_path: str) -> None:
    """
    Extracts e-commerce sales data from a local Excel file,
    converts it to CSV, and saves it for downstream processing.
    """

    try:
        logging.info("Starting data extraction process (LOCAL FILE MODE)")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file not found: {source_path}")

        # Read Excel
        df = pd.read_excel(source_path)

        if df.empty:
            raise ValueError("Extracted dataset is empty")

        # Save as CSV
        df.to_csv(output_path, index=False)

        logging.info(f"Data successfully extracted and saved to {output_path}")
        logging.info(f"Total records extracted: {len(df)}")

    except Exception as e:
        logging.error("Error during data extraction", exc_info=True)
        raise
