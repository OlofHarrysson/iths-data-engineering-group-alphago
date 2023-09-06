from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def write_hello():
    with open(
        r"C:\Users\jonas\Documents\GitHub\iths-data-engineering-group-alphago\airflow_tests\hello.txt",
        "w",
    ) as f:
        f.write("Hello, World!")


def append_text():
    with open(
        r"C:\Users\jonas\Documents\GitHub\iths-data-engineering-group-alphago\airflow_tests\hello.txt",
        "a",
    ) as f:
        f.write("\nAirflow Test Succesful!")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "hello_world_dag",
    default_args=default_args,
    description="A simple Hello World DAG",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 9, 6),
    catchup=False,
)

t1 = PythonOperator(
    task_id="write_hello",
    python_callable=write_hello,
    dag=dag,
)

t2 = PythonOperator(
    task_id="append_text",
    python_callable=append_text,
    dag=dag,
)

t1 >> t2
