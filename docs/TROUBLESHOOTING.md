# Troubleshooting Guide

This guide covers common issues encountered during the development and execution of the pipeline.

## Docker Issues

### 1. `Bind for 0.0.0.0:1433 failed: port is already allocated`
*   **Cause**: You have a local SQL Server instance running or another container using port 1433.
*   **Fix**: Stop the local service or change the port mapping in `docker-compose.yml` (e.g., `1434:1433`).

### 2. Container exits immediately
*   **Cause**: Usually missing environment variables or configuration files.
*   **Fix**: Check logs with `docker-compose logs <service_name>`.

## DBT Issues

### 1. `Login failed for user 'sa'`
*   **Cause**: Incorrect password in `profiles.yml` or the SQL Server container hasn't finished setting up the SA password.
*   **Fix**: Ensure the password in `profiles.yml` matches `SA_PASSWORD` in `docker-compose.yml`. Wait a minute for SQL Server to warm up.

### 2. `Relation not found` or `Invalid object name`
*   **Cause**: The raw tables don't exist in the source database yet.
*   **Fix**: Ensure your source data has been sowed/migrated. If using a fresh container, you may need to restore the AdventureWorks backup (check the setup scripts).

### 3. Compilation Error
*   **Cause**: Syntax error in SQL or Jinja.
*   **Fix**: Run `dbt compile` to see the generated SQL in `target/compiled/`.

## Airflow Issues

### 1. DAG not appearing in UI
*   **Cause**: Parse error in the Python file or the scheduler is stuck.
*   **Fix**:
    *   Check scheduler logs: `docker-compose logs airflow-scheduler`.
    *   Run `python airflow/dags/dbt_dag.py` locally to check for syntax errors.

### 2. Task stays in "Queued" state
*   **Cause**: Scheduler not running or no worker slots available.
*   **Fix**: Restart the scheduler: `docker-compose restart airflow-scheduler`.

## General Debugging

To get a shell inside a container for manual testing:

```bash
# For DBT
docker-compose run --rm --entrypoint bash dbt

# For Airflow Worker/Scheduler
docker-compose exec airflow-scheduler bash
```
