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


sum_types = ["tech", "ntech", "swe"]


@task(task_id="summarize_mit")
def summarize_mit_task():
    new_articles = summarize.main(source="mit")
    for sum_type in sum_types[1:]:
        summarize.main(source="mit", sum_type=sum_type)

    return new_articles


@task(task_id="summarize_aws")
def summarize_aws_task():
    new_articles = summarize.main(source="aws")
    for sum_type in sum_types[1:]:
        summarize.main(source="aws", sum_type=sum_type)

    return new_articles


@task(task_id="summarize_openai")
def summarize_openai_task() -> None:
    new_articles = summarize.main(source="openai")
    for sum_type in sum_types[1:]:
        summarize.main(source="openai", sum_type=sum_type)

    return new_articles


@task(task_id="discord_bot")
def discord_bot_task(mit_articles, aws_articles, openai_articles) -> None:
    for sum_type in sum_types:
        discord_bot.main(source="mit", articles=mit_articles, sum_type=sum_type)
        discord_bot.main(source="aws", articles=aws_articles, sum_type=sum_type)
        discord_bot.main(source="openai", articles=openai_articles, sum_type=sum_type)


@dag(
    dag_id="test_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def test_pipeline() -> None:
    mit = summarize_mit_task()
    aws = summarize_aws_task()
    openai = summarize_openai_task()
    # task7 = discord_bot_task(task4, task5, task6)
    # task7 = discord_bot_task(task4)
    (
        download_blogs_from_rss_task()
        >> extract_articles_task()
        >> webscraper_task()
        >> mit
        >> aws
        >> openai
        >> discord_bot_task(mit, aws, openai)
    )


# register DAG
test_pipeline()
