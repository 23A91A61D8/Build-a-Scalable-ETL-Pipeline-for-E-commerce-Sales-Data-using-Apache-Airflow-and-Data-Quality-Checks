# Build-a-Scalable-ETL-Pipeline-for-E-commerce-Sales-Data-using-Apache-Airflow-and-Data-Quality-Checks

---

## Project Overview

This project implements a scalable and production-style ETL (Extract, Transform, Load) pipeline for e-commerce sales transaction data using Apache Airflow. The pipeline extracts raw sales data, performs data cleaning and enrichment, applies data quality checks, and loads the processed data into a PostgreSQL data warehouse designed using a star schema.

The solution is fully containerized using Docker and Docker Compose, ensuring reproducibility and ease of deployment.

---

## Tech Stack

- Apache Airflow 2.6.3
- Docker & Docker Compose
- Python 3.9
- Pandas
- PostgreSQL
- SQLAlchemy
- psycopg2
- Pytest

---

## Project Structure
Build-a-Scalable-ETL-Pipeline/
│
├── dags/
│ └── ecom_etl_dag.py
│
├── src/
│ └── etl_scripts/
│ ├── extract.py
│ ├── transform.py
│ └── load.py
│
├── ddl/
│ ├── create_dim_customers.sql
│ ├── create_dim_products.sql
│ └── create_fact_sales.sql
│
├── tests/
│ ├── unit/
│ │ └── test_transformations.py
│ └── integration/
│ └── test_data_quality.py
│
├── data/
│ └── online_retail.xlsx
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── ARCHITECTURE.md

---

## Dataset

- Dataset Name: Online Retail Dataset
- Source: UCI Machine Learning Repository
- Format: Excel (.xlsx)
- Stored locally at:
data/online_retail.xlsx


The dataset is mounted into Airflow containers to avoid external network dependency.

---

## ETL Workflow

### Extract
- Reads the Excel dataset from the mounted data directory
- Converts it into CSV format
- Stores it in a temporary staging location

### Transform
- Handles missing values
- Removes duplicate records
- Converts data types
- Calculates derived column:
  - `total_item_price = Quantity * UnitPrice`
- Generates unique `customer_id` values

### Load
- Loads data into PostgreSQL
- Uses UPSERT logic for idempotent dimension loading
- Loads fact data incrementally to avoid duplication

---

## Data Warehouse Schema

### dim_customers
- customer_id (Primary Key)
- country
- last_updated_at

### dim_products
- product_id (Primary Key)
- description
- unit_price
- last_updated_at

### fact_sales
- sale_id (Primary Key)
- invoice_no
- customer_id (Foreign Key)
- product_id (Foreign Key)
- quantity
- total_item_price
- invoice_date
- processed_at

---

## Data Quality Checks

### Pre-load Checks
- Extracted data must not be empty
- No NULL values in critical columns (InvoiceNo, StockCode)
- Quantity and UnitPrice must be positive

### Post-load Checks
- Primary key uniqueness in dimension tables
- Referential integrity between fact and dimension tables

Pipeline execution stops if any critical check fails.

---

## Incremental Loading

- Fact table loads only new or unprocessed records
- Prevents duplicate sales records across DAG runs
- Uses timestamps and invoice identifiers for filtering

---

## Testing

### Unit Tests
- Located in `tests/unit/test_transformations.py`
- Tests transformation logic such as:
  - Price calculation
  - Quantity validation
  - Non-empty dataset checks

### Integration Tests
- Located in `tests/integration/test_data_quality.py`
- Tests data quality validation functions

All tests are implemented using Pytest.

---

## Docker Setup

### Start Services
docker-compose up -d

### Initialize Airflow Database
docker compose run --rm airflow-webserver airflow db init


### Create Admin User
docker compose run --rm airflow-webserver airflow users create
--username admin
--password admin
--firstname Lakshmi
--lastname V
--role Admin
--email admin@example.com


---

## Access Airflow UI

- URL: http://localhost:8080
- Username: admin
- Password: admin

---

## Running the DAG

1. Open Airflow UI
2. Enable `ecom_etl_dag`
3. Trigger the DAG manually
4. Monitor task logs
5. Verify data in PostgreSQL tables

---

## Architecture

Refer to `ARCHITECTURE.md` for a detailed explanation of:
- System components
- Data flow
- ETL orchestration design

---

## Task Completion Summary

- Dockerized Airflow environment: Completed
- ETL pipeline implementation: Completed
- Star schema data warehouse: Completed
- Data quality checks: Implemented
- Incremental loading: Implemented
- Unit and integration tests: Implemented
- Documentation: Completed

---

## Conclusion

This project demonstrates a real-world, production-ready ETL pipeline using Apache Airflow, applying data engineering best practices including modular design, data quality validation, incremental loading, and containerized deployment.

