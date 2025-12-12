from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "dataops",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": ["data-team@company.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "data_quality_validation",
    default_args=default_args,
    description="Run Great Expectations data quality validations",
    schedule_interval="0 */6 * * *",  # Every 6 hours
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["data-quality", "great-expectations"],
)


def run_ge_checkpoint(checkpoint_name, **context):
    """Run a Great Expectations checkpoint"""
    from great_expectations.data_context import DataContext

    # Initialize Data Context
    context_root_dir = "/opt/airflow/gx"
    data_context = DataContext(context_root_dir=context_root_dir)

    # Run checkpoint
    print(f"Running checkpoint: {checkpoint_name}")
    result = data_context.run_checkpoint(checkpoint_name=checkpoint_name)

    # Check results
    if not result["success"]:
        failed_validations = []
        for run_result in result.run_results.values():
            if not run_result["success"]:
                failed_validations.append(run_result)

        error_msg = f"Data quality validation failed for {checkpoint_name}"
        print(f"❌ {error_msg}")
        print(f"Failed validations: {len(failed_validations)}")
        raise Exception(error_msg)

    print(f"✅ Checkpoint {checkpoint_name} passed successfully")
    return result


# Tasks
validate_customers = PythonOperator(
    task_id="validate_customer_data",
    python_callable=run_ge_checkpoint,
    op_kwargs={"checkpoint_name": "customer_checkpoint"},
    dag=dag,
)

validate_orders = PythonOperator(
    task_id="validate_sales_order_data",
    python_callable=run_ge_checkpoint,
    op_kwargs={"checkpoint_name": "sales_order_checkpoint"},
    dag=dag,
)

generate_docs = BashOperator(
    task_id="generate_data_docs",
    bash_command="cd /opt/airflow/gx && great_expectations docs build",
    dag=dag,
)

# Dependencies
[validate_customers, validate_orders] >> generate_docs
