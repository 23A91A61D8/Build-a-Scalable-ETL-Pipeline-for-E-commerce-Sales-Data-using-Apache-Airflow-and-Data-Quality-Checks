# -------------------- IMPORTANT IMPORT FIX --------------------
import sys
import os

# Add project root so Airflow can find src/
sys.path.append(os.path.abspath("/opt/airflow"))
# -------------------------------------------------------------

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

from src.etl_scripts.extract import extract_sales_data
from src.etl_scripts.transform import transform_sales_data
from src.etl_scripts.load import (
    load_dim_customers,
    load_dim_products,
    load_fact_sales,
)

# -------------------- CONSTANTS --------------------

RAW_DATA_PATH = "/tmp/data/raw_sales.csv"
TRANSFORMED_DATA_PATH = "/tmp/data/transformed_sales.csv"

SOURCE_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

# -------------------- DAG DEFINITION --------------------

with DAG(
    dag_id="ecom_etl_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="Scalable ETL pipeline for E-commerce sales data",
) as dag:

    # Start task
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    # Extract task
    extract_task = PythonOperator(
    task_id="extract_sales_data",
    python_callable=extract_sales_data,
    op_kwargs={
        "source_path": "/opt/airflow/data/online_retail.xlsx",
        "output_path": "/tmp/data/raw_sales.csv"
    },
)


    # Transform task
    transform_task = PythonOperator(
        task_id="transform_sales_data",
        python_callable=transform_sales_data,
        op_args=[RAW_DATA_PATH, TRANSFORMED_DATA_PATH],
    )

    # Load dimension tables
    load_customers_task = PythonOperator(
        task_id="load_dim_customers",
        python_callable=load_dim_customers,
        op_args=[TRANSFORMED_DATA_PATH],
    )

    load_products_task = PythonOperator(
        task_id="load_dim_products",
        python_callable=load_dim_products,
        op_args=[TRANSFORMED_DATA_PATH],
    )

    # Load fact table
    load_fact_task = PythonOperator(
        task_id="load_fact_sales",
        python_callable=load_fact_sales,
        op_args=[TRANSFORMED_DATA_PATH],
    )

    # End task
    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # -------------------- TASK DEPENDENCIES --------------------

    start_pipeline >> extract_task >> transform_task
    transform_task >> [load_customers_task, load_products_task]
    [load_customers_task, load_products_task] >> load_fact_task >> end_pipeline
