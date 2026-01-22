# ETL Pipeline Architecture – E-commerce Sales Data

## Overview

This document describes the high-level architecture of the **Scalable ETL Pipeline for E-commerce Sales Data** implemented using Apache Airflow, Docker, and PostgreSQL. The architecture follows modern data engineering best practices, ensuring scalability, reliability, and maintainability.

The pipeline automates the movement of raw transactional data from a source file into a structured data warehouse using a star schema, while enforcing data quality checks and supporting incremental data loading.

---

## High-Level Architecture Components
+----------------------+
| E-commerce Dataset |
| (Excel / CSV File) |
+----------+-----------+
|
v
+----------------------+
| Airflow Extract |
| Task (Python) |
+----------+-----------+
|
v
+----------------------+
| Staging Layer |
| (Local CSV Storage) |
+----------+-----------+
|
v
+----------------------+
| Transform Layer |
| (Pandas Processing) |
+----------+-----------+
|
v
+----------------------+
| Data Quality Checks |
| (Pre & Post Load) |
+----------+-----------+
|
v
+----------------------+
| PostgreSQL Data |
| Warehouse (Star) |
+----------------------+


---

## Component Description

### 1. Data Source
- Public e-commerce sales dataset (Online Retail Dataset)
- Stored locally in the project directory and mounted into Docker containers
- Eliminates dependency on external network access

---

### 2. Apache Airflow
Apache Airflow is used as the orchestration engine.

Responsibilities:
- Scheduling ETL workflows
- Managing task dependencies
- Handling retries and failures
- Logging execution details

Airflow Components:
- **Webserver**: UI for monitoring DAGs
- **Scheduler**: Triggers DAG runs
- **Workers**: Execute ETL tasks
- **Metadata Database**: Stores Airflow state (PostgreSQL)

---

### 3. Extract Layer
- Implemented using a PythonOperator
- Reads Excel file from mounted data directory
- Converts raw data into CSV format
- Stores extracted data in a staging location

Key Characteristics:
- Idempotent
- Logged
- Error-handled

---

### 4. Staging Layer
- Temporary storage for extracted and transformed data
- Implemented as local CSV files inside the Airflow container
- Separates raw data from transformed data to simplify debugging

---

### 5. Transform Layer
- Implemented using Pandas
- Handles:
  - Missing values
  - Duplicate records
  - Data type conversions
  - Derived metric calculation (`total_item_price`)
  - Customer ID generation

Design Principle:
- Modular functions
- Testable logic
- Single responsibility per function

---

### 6. Data Quality Layer

#### Pre-load Checks
- Dataset is not empty
- No nulls in critical columns
- Quantity and UnitPrice are valid

#### Post-load Checks
- Primary key uniqueness
- Referential integrity between fact and dimensions

Failures immediately stop the pipeline to prevent bad data propagation.

---

### 7. Load Layer (Data Warehouse)

#### Database: PostgreSQL

Schema Design:
- Star schema optimized for analytics

Tables:
- `dim_customers`
- `dim_products`
- `fact_sales`

Features:
- UPSERT logic for dimension tables
- Incremental loading for fact table
- Foreign key enforcement

---

## Incremental Loading Strategy

- Tracks processed records using invoice identifiers and timestamps
- Ensures only new or updated records are loaded
- Prevents duplicate entries across DAG runs
- Improves performance and scalability

---

## Containerization & Deployment

### Docker
- All services run in isolated containers
- Ensures environment consistency

### Docker Compose
- Orchestrates:
  - PostgreSQL
  - Airflow Webserver
  - Airflow Scheduler
  - Airflow Workers

Volumes:
- DAGs
- Source code
- Data directory
- PostgreSQL persistence

---

## Fault Tolerance & Reliability

- Task retries configured in Airflow
- Robust exception handling in ETL scripts
- Data quality gates prevent corrupt data
- Logs available for every task execution

---

## Scalability Considerations

- Horizontal scaling via Airflow workers
- Incremental loading reduces data volume per run
- Modular ETL logic allows future extensions
- Compatible with cloud migration (AWS, GCP, Azure)

---

## Summary

This architecture provides a robust, scalable, and production-ready ETL pipeline that mirrors real-world data engineering systems. It ensures clean data ingestion, reliable orchestration, strong data quality enforcement, and analytical-ready storage using industry-standard tools.

---
