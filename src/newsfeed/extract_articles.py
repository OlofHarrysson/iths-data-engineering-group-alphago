import argparse
import re
import shlex
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from newsfeed.datatypes import BlogInfo


def create_uuid_from_string(title):
    assert isinstance(title, str)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, title))


def load_metadata(blog_name):
    metadata_path = Path("data/data_lake") / blog_name / "metadata.xml"
    with open(metadata_path, encoding="utf-8") as f:
        xml_text = f.read()

    parsed_xml = BeautifulSoup(xml_text, "xml")
    return parsed_xml


# removes invalid characters in filename, "/", ">" etc
def sanitize_filename(filename):
    valid_filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    # truncates cleaned-up filename to ensure it's not too long
    return valid_filename[:250]


def extract_articles_from_xml(parsed_xml):
    articles = []
    for item in parsed_xml.find_all("item"):
        raw_blog_text = item.find("content:encoded").text
        soup = BeautifulSoup(raw_blog_text, "html.parser")
        blog_text = soup.get_text()
        title = item.title.text
        unique_id = create_uuid_from_string(title)
        article_info = BlogInfo(
            unique_id=unique_id,
            title=title,
            description=item.description.text,
            link=item.link.text,
            blog_text=blog_text,
            published=pd.to_datetime(item.pubDate.text).date(),
            timestamp=datetime.now(),
        )
        articles.append(article_info)

    return articles


def save_articles(articles, blog_name):
    save_dir = Path("data/data_warehouse", blog_name, "articles")
    save_dir.mkdir(exist_ok=True, parents=True)
    for article in articles:
        sanitized_filename = sanitize_filename(article.get_filename())
        save_path = save_dir / sanitized_filename
        print(f"Saving article to {save_path}")  # Debug line
        with open(save_path, "w") as f:
            f.write(article.json(indent=2))


def main(blog_name):
    print(f"Processing {blog_name}")
    parsed_xml = load_metadata(blog_name)
    articles = extract_articles_from_xml(parsed_xml)
    save_articles(articles, blog_name)
    print(f"Done processing {blog_name}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blog_name", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(blog_name=args.blog_name)
