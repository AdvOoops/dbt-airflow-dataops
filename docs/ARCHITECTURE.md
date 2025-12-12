# System Architecture

## Overview

This project implements a modern DataOps pipeline designed to transform raw data into business-ready insights. The architecture follows a robust Extract, Load, Transform (ELT) pattern, leveraging containerization for consistency and scalability.

## Architecture Diagram

The following diagram illustrates the high-level architecture and data flow of the system:

```mermaid
graph TD
    subgraph Infrastructure [Docker Runtime Environment]
        style Infrastructure fill:#f9f9f9,stroke:#333,stroke-width:2px

        subgraph Orchestration [Orchestration Layer]
            style Orchestration fill:#e1f5fe,stroke:#01579b
            AF_Web[Airflow Webserver]
            AF_Sch[Airflow Scheduler]
            AF_Meta[(Airflow Metadata DB)]
        end

        subgraph Data_Processing [Data Processing Layer]
            style Data_Processing fill:#e8f5e9,stroke:#2e7d32
            DBT[DBT Core Container]
        end

        subgraph Storage [Storage Layer]
            style Storage fill:#fff3e0,stroke:#ef6c00
            SQL[SQL Server Sources]
            DW[Data Warehouse Target]
        end
    end

    %% Data Flow Relationships
    AF_Sch -->|Trigger & Monitor| DBT
    AF_Web -->|Interact| AF_Sch
    AF_Sch -->|Read/Write State| AF_Meta

    DBT -->|Read Source Data| SQL
    DBT -->|Transform & Load| DW

    %% User Interaction
    User((Data Engineer)) -->|Deploy Code| GitHub[GitHub Repo]
    User -->|Monitor| AF_Web
    GitHub -->|CI/CD| DBT
```

## Data Flow

1.  **Ingestion & Staging (Bronze Layer)**:
    *   DBT connects to the source SQL Server database.
    *   Data is read from raw `AdventureWorks` tables.
    *   Basic cleaning and standardization rules are applied.
    *   Result: `staging_*` views/tables accessible in the warehouse.

2.  **Transformation (Silver Layer)**:
    *   DBT reads from the Bronze layer models.
    *   Business logic, filtering, and joins are applied (e.g., joining Orders with Customers).
    *   Result: Intermediate models representing business entities.

3.  **Mart Creation (Gold Layer)**:
    *   Aggregates and complex metrics are calculated from Silver models.
    *   Data is structured for specific analytic use cases (e.g., Sales Dashboard).
    *   Result: High-performance tables ready for consumption by BI tools.

## Key Components

### 1. Source System: SQL Server 2019
*   **Role**: Acts as the operational database containing raw business data (AdventureWorks).
*   **Deployment**: Runs in a Docker container alongside the pipeline.

### 2. Transformation Engine: DBT (Data Build Tool)
*   **Role**: Performs T (Transform) in ELT. Compiles SQL models and runs them against the target database.
*   **Key Features Used**:
    *   Modular Data Modeling (Bronze/Silver/Gold).
    *   Data Testing (Schema & Custom tests).
    *   Documentation generation.

### 3. Orchestration: Apache Airflow
*   **Role**: Manages the schedule and execution dependencies of the pipeline.
*   **Workflow**:
    *   Triggers DBT jobs on a defined schedule (e.g., daily).
    *   Retries failed tasks.
    *   Alerts on failure.

### 4. CI/CD: GitHub Actions
*   **Role**: Automates code quality checks and deployment.
*   **Pipeline**:
    *   **CI**: Lints SQL/Python code, runs DBT tests on Pull Requests.
    *   **CD**: Automatically runs the transformation pipeline upon merge to `main`.
