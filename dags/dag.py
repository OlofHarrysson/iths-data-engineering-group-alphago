from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import discord_bot, download_blogs_from_rss, extract_articles, summarize


@task(task_id="download_blogs_from_rss")
def download_blogs_from_rss_task() -> None:
    download_blogs_from_rss.main(blog_name="mit")
    # download_blogs_from_rss.main(blog_name="aws")


@task(task_id="extract_articles")
def extract_articles_task() -> None:
    extract_articles.main(blog_name="mit")


@task(task_id="summarize")
def summarize_task() -> None:
    summarize.main(source="mit", sum_type="tech")


@task(task_id="discord_bot")
def discord_bot_task() -> None:
    discord_bot.main(source="mit")


@dag(
    dag_id="test_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def test_pipeline() -> None:
    # hello_task() >> download_blogs_from_rss_task()
    # download_blogs_from_rss_task()
    (
        download_blogs_from_rss_task()
        >> extract_articles_task()
        >> summarize_task()
        >> discord_bot_task()
    )


# register DAG
test_pipeline()
