# Data Model Documentation

This document outlines the data architecture and the specific models implemented in the DBT project.

## Modeling Strategy: Medallion Architecture

We follow a 3-layer approach (Bronze -> Silver -> Gold) to ensure data quality and lineage.

| Layer | Name | Purpose | Materialization |
|-------|------|---------|-----------------|
| **Bronze** | Staging | Raw data ingestion, renaming, and type casting. 1:1 with source tables. | View |
| **Silver** | Intermediate | Data cleaning, joining, and business logic application. Entity-centric. | Table |
| **Gold** | Marts | Aggregated, dimensional models ready for analytics and reporting. | Table |

## 1. Bronze Layer (Staging)

Located in `dbt/models/staging/`.

*   **Goal**: Clean up raw column names (snake_case), cast types, and remove sensitive data if necessary.
*   **Key Models**:
    *   `stg_sales_orders`: Extracts from `SalesOrderHeader` and `SalesOrderDetail`.
    *   `stg_customers`: Extracts from `Customer` table.
    *   `stg_products`: Extracts from `Product` table.

## 2. Silver Layer (Intermediate)

Located in `dbt/models/marts/core` (or `intermediate` depending on specific logic).

*   **Goal**: Create robust business entities.
*   **Key Models**:
    *   `dim_customers`: Enriched customer data, joined with geographic info.
    *   `fct_orders`: Order facts joined with customer keys, calculating net totals.

## 3. Gold Layer (Marts)

Located in `dbt/models/marts/finance` or `sales`.

*   **Goal**: Provide answers to business questions.
*   **Key Models**:
    *   `mart_monthly_revenue`: Aggregates revenue by month and territory.
    *   `mart_best_selling_products`: Ranks products by sales volume.

## Data Lineage

The data flows as follows:

1.  **Source**: `AdventureWorks.Sales.*`
2.  **Staging**: `stg_sales_orders` -> `stg_customers`
3.  **Intermediate**: `int_order_details` (Joins orders with products)
4.  **Mart**: `fct_monthly_sales`

You can visualize the full lineage by running:

```bash
dbt docs generate
dbt docs serve
```
