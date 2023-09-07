from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import (
    discord_bot,
    download_blogs_from_rss,
    extract_articles,
    summarize,
    webscraper,
)


# openai only
@task(task_id="webscraper")
def webscraper_task() -> None:
    webscraper.main()


# downnload blogs
@task(task_id="download_blogs_from_rss")
def download_blogs_from_rss_task() -> None:
    download_blogs_from_rss.main(blog_name="mit")
    download_blogs_from_rss.main(blog_name="aws")


# extract articles
@task(task_id="extract_articles")
def extract_articles_task() -> None:
    extract_articles.main(blog_name="mit")
    extract_articles.main(blog_name="aws")


# technical summaries
@task(task_id="summarize_tech")
def summarize_tech_task() -> None:
    summarize.main(source="mit", sum_type="tech")
    # summarize.main(source="aws", sum_type="tech")
    summarize.main(source="openai", sum_type="tech")


# non-technical summaries
@task(task_id="summarize_non_tech")
def summarize_non_tech_task() -> None:
    summarize.main(source="mit", sum_type="ntech")
    # summarize.main(source="aws", sum_type="ntech")
    summarize.main(source="openai", sum_type="ntech")


# swedish summaries
@task(task_id="summarize_swe")
def summarize_swe_task() -> None:
    summarize.main(source="mit", sum_type="swe")
    # summarize.main(source="aws", sum_type="swe")
    summarize.main(source="openai", sum_type="swe")


# discord bot - only sends tech summaries atm, can fix by adding a new task
@task(task_id="discord_bot")
def discord_bot_task() -> None:
    discord_bot.main(
        source="mit",
        ix=1,
        sum_type="tech",
    )
    # discord_bot.main(source="aws", ix=1, sum_type="tech",)
    discord_bot.main(
        source="openai",
        ix=1,
        sum_type="tech",
    )


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
        >> webscraper_task()
        >> summarize_tech_task()
        >> summarize_non_tech_task()
        >> summarize_swe_task()
        >> discord_bot_task()
    )


# register DAG
test_pipeline()
