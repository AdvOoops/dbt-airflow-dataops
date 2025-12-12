# Project Setup Guide

This guide will help you set up the DataOps pipeline environment on your local machine.

## Prerequisites

Before starting, ensure you have the following installed:

*   **Docker Desktop** (or Docker Engine + Compose on Linux)
    *   *Verification*: `docker --version` && `docker-compose --version`
*   **Git**
    *   *Verification*: `git --version`
*   **VS Code** (Optional but recommended)

## Installation Steps

### 1. Clone the Repository

Open your terminal and run:

```bash
git clone <repository_url>
cd dbt_airflow_project
```

### 2. Configure Environment

Typically, you might need a `.env` file. For this lab, the configuration is mostly contained within `docker-compose.yml` and `profiles.yml`.

Ensure that `dbt/profiles.yml` matches the credentials in `docker-compose.yml`.

### 3. Start Infrastructure

We use Docker Compose to spin up SQL Server, Airflow, and the utility containers.

```bash
# Start all services in detached mode
docker-compose up -d
```

**Wait for 2-3 minutes** for SQL Server and Airflow to fully initialize. You can check the status with:

```bash
docker-compose ps
```

All services (`sqlserver`, `airflow-webserver`, `airflow-scheduler`, `postgres`) should be "Up" or "Running".

### 4. Initialize Airflow (First Time Only)

If Airflow doesn't start correctly, you might need to initialize the database:

```bash
docker-compose run --rm airflow-webserver airflow db init
docker-compose run --rm airflow-webserver airflow users create \
    --username airflow \
    --password airflow \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

### 5. Initialize DBT

Install required DBT dependencies (packages like `dbt-utils`):

```bash
docker-compose run --rm dbt dbt deps
```

### 6. Verify Connection

Test if DBT can connect to the SQL Server database:

```bash
docker-compose run --rm dbt dbt debug
```

If you see `All checks passed!`, you are ready to go.

## Running the Pipeline

### Option A: Manual Run via CLI

You can manually trigger the DBT transformation:

```bash
# Run all models
docker-compose run --rm dbt dbt run

# Run tests
docker-compose run --rm dbt dbt test
```

### Option B: Trigger via Airflow

1.  Open your browser and navigate to `http://localhost:8080`.
2.  Login with `airflow` / `airflow`.
3.  Find the `dbt_transform` DAG.
4.  Toggle the DAG to **ON**.
5.  Click the "Play" button (Trigger DAG) to start a run manually.
6.  Click on the DAG name to verify the graph view and task success.

## Project Structure Check

After setup, your directory should look distinctively like this:

```text
dbt_airflow_project/
├── airflow/            # Airflow DAGs and configs
├── dbt/                # DBT Models and tests
├── docs/               # This documentation
├── docker-compose.yml  # Infrastructure definition
└── README.md           # Entry point
```
