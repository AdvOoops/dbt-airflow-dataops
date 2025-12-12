# Great Expectations Data Quality Framework

This directory contains the Great Expectations configuration for data quality validation.

## Structure

```
great_expectations/
├── great_expectations.yml     # Main configuration file
├── expectations/              # Expectation suites
│   ├── customer_suite.json
│   └── sales_order_suite.json
├── checkpoints/              # Validation checkpoints
│   ├── customer_checkpoint.yml
│   └── sales_order_checkpoint.yml
└── uncommitted/              # Generated files (gitignored)
    ├── validations/
    └── data_docs/
```

## Setup

1. Install Great Expectations in the DBT container:
```bash
docker exec dbt_airflow_project-dbt-1 pip install great-expectations==0.18.8 sqlalchemy==1.4.48
```

2. Install in Airflow container:
```bash
docker exec dbt_airflow_project-airflow-scheduler-1 pip install great-expectations==0.18.8 sqlalchemy==1.4.48
```

## Running Validations

### Manual Execution

Run a checkpoint manually:
```bash
# In DBT container
docker exec dbt_airflow_project-dbt-1 bash -c "cd /usr/app/great_expectations && great_expectations checkpoint run customer_checkpoint"
```

### Via Airflow

The `data_quality_validation` DAG runs every 6 hours and executes all checkpoints.

View in Airflow UI: http://localhost:8080

## Expectation Suites

### Customer Quality Suite
- Table row count between 100 and 100,000
- CustomerID column exists
- CustomerID values are unique
- CustomerID has no nulls
- AccountNumber has no nulls

### Sales Order Quality Suite
- SalesOrderID values are unique
- SalesOrderID has no nulls
- TotalDue is between 0 and 1,000,000
- OrderDate has no nulls

## Adding New Expectations

1. Create a new expectation suite JSON file in `expectations/`
2. Create a corresponding checkpoint YAML file in `checkpoints/`
3. Add a new task in `airflow/dags/data_quality_dag.py`

## Viewing Results

Generate and view data docs:
```bash
docker exec dbt_airflow_project-dbt-1 bash -c "cd /usr/app/great_expectations && great_expectations docs build"
```

The documentation will be available in `uncommitted/data_docs/local_site/`

## Troubleshooting

### Connection Issues
Check the connection string in `great_expectations.yml`:
```yaml
connection_string: mssql+pyodbc://sa:YourStrong@Passw0rd@sqlserver:1433/AdventureWorks2014?driver=ODBC+Driver+17+for+SQL+Server
```

### Validation Failures
Review the validation results in `uncommitted/validations/` or check Airflow logs.

## References

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Expectation Gallery](https://greatexpectations.io/expectations)
