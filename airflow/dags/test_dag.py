from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def say_hello() -> None:
    print("Hello from your first Airflow DAG")


with DAG(
    dag_id="test_dag",
    start_date=datetime(2026, 4, 1),
    schedule=None,
    catchup=False,
    tags=["test"],
):
    hello_task = PythonOperator(
        task_id="say_hello",
        python_callable=say_hello,
    )