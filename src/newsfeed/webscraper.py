import json
from datetime import datetime
from pathlib import Path
from time import sleep
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from newsfeed.extract_articles import create_uuid_from_string, sanitize_filename

data_warehouse_dir = Path("data/data_warehouse/openai/articles")
data_warehouse_dir.mkdir(parents=True, exist_ok=True)


def main():
    # Step 1: Fetch the main blog page and extract article URLs
    response = requests.get("https://openai.com/blog")
    if response.status_code != 200:
        print(f"Failed to get the main page, status code: {response.status_code}")
        exit()

    # find links to articles
    soup = BeautifulSoup(response.content, "html.parser")
    for a_tag in soup.find_all("a"):
        h3_tag = a_tag.find("h3")
        if h3_tag:
            article = {}
            article["link"] = urljoin("https://openai.com/blog", a_tag.get("href"))
            article["title"] = h3_tag.text

            sleep(0.2)

            # Fetch and parse individual artiles
            response = requests.get(article["link"])
            if response.status_code != 200:
                print(
                    f"Failed to get the article: {article['link']}, status code: {response.status_code}"
                )
                continue

            soup = BeautifulSoup(response.content, "html.parser")

            # find publishing date
            date_tag = soup.find("span", {"class": "f-meta-2"})

            if date_tag:
                datetime_object = datetime.strptime(date_tag.text, "%B %d, %Y")
                formatted_date_str = datetime_object.strftime("%Y-%m-%d")
                article["published"] = formatted_date_str

            # find article content
            article_content_tag = soup.find("div", {"id": "content"})

            if article_content_tag:
                article["blog_text"] = article_content_tag.text
                article["description"] = ""
                article["unique_id"] = create_uuid_from_string(article["title"])

                sanitized_filename = sanitize_filename(f"{article['title']}.json")

                # save to jsonfile
                json_file_path = data_warehouse_dir / sanitized_filename
                with json_file_path.open("w") as f:
                    json.dump(article, f, indent=2)
            else:
                print(f"Could not find content for article at {article['link']}")


if __name__ == "__main__":
    main()
