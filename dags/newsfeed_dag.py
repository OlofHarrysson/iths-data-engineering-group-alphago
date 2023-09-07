from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from newsfeed.download_blogs_from_rss import airflow_dag_argument
from newsfeed.extract_articles import airflow_dag_argument_extract

# from extract_articles import extract_articles
# from summarize import summarize
# from discord_bot import discord_bot

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "download_rss_dag",
    default_args=default_args,
    description="Download blogs from rss dag",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 9, 6),
    catchup=False,
)

# download blogs
for arg in ["--blog_name mit", "--blog_name aws"]:
    t1 = PythonOperator(
        task_id=f"download_blogs_from_rss{arg.split()[-1]}",
        python_callable=airflow_dag_argument,
        op_args=[arg],
        dag=dag,
    )

# extract_articles
for arg in ["--blog_name mit", "--blog_name aws"]:
    t2 = PythonOperator(
        task_id=f"extract_articles{arg.split()[-1]}",
        python_callable=airflow_dag_argument_extract,
        op_args=[arg],
        dag=dag,
    )

t1 >> t2
