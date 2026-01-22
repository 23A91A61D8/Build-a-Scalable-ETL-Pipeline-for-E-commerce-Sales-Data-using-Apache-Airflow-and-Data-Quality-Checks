import pandas as pd
import logging
from sqlalchemy import create_engine, text


def get_db_engine():
    """
    Creates and returns a SQLAlchemy engine for PostgreSQL.
    """
    db_uri = "postgresql+psycopg2://airflow:airflow@postgres:5432/ecom_dw"
    return create_engine(db_uri)


def load_dim_customers(transformed_path: str) -> None:
    """
    Loads customer dimension data into dim_customers table.
    """
    try:
        logging.info("Loading dim_customers")

        engine = get_db_engine()
        df = pd.read_csv(transformed_path)

        dim_customers = (
            df[["customer_id", "Country"]]
            .drop_duplicates()
            .rename(columns={"Country": "country"})
        )

        dim_customers.to_sql(
            "dim_customers",
            engine,
            if_exists="append",
            index=False,
            method="multi",
        )

        logging.info("dim_customers loaded successfully")

    except Exception as e:
        logging.error("Error loading dim_customers")
        raise e


def load_dim_products(transformed_path: str) -> None:
    """
    Loads product dimension data into dim_products table.
    """
    try:
        logging.info("Loading dim_products")

        engine = get_db_engine()
        df = pd.read_csv(transformed_path)

        dim_products = (
            df[["StockCode", "Description", "UnitPrice"]]
            .drop_duplicates()
            .rename(
                columns={
                    "StockCode": "product_id",
                    "Description": "description",
                    "UnitPrice": "unit_price",
                }
            )
        )

        dim_products.to_sql(
            "dim_products",
            engine,
            if_exists="append",
            index=False,
            method="multi",
        )

        logging.info("dim_products loaded successfully")

    except Exception as e:
        logging.error("Error loading dim_products")
        raise e


def load_fact_sales(transformed_path: str) -> None:
    """
    Loads fact sales data into fact_sales table.
    """
    try:
        logging.info("Loading fact_sales")

        engine = get_db_engine()
        df = pd.read_csv(transformed_path)

        fact_sales = df.rename(
            columns={
                "InvoiceNo": "invoice_no",
                "StockCode": "product_id",
                "InvoiceDate": "invoice_date",
                "Quantity": "quantity",
            }
        )[
            [
                "invoice_no",
                "customer_id",
                "product_id",
                "quantity",
                "total_item_price",
                "invoice_date",
            ]
        ]

        fact_sales.to_sql(
            "fact_sales",
            engine,
            if_exists="append",
            index=False,
            method="multi",
        )

        logging.info("fact_sales loaded successfully")

    except Exception as e:
        logging.error("Error loading fact_sales")
        raise e
