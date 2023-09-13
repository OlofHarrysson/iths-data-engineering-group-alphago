import json
import os
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

from newsfeed import dashboard_layout, summarize

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
    # makes responsivity possible (different web browser sizes)
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
    # suppress_callback_exceptions=True
)

app.layout = dashboard_layout.LayoutHandler().create_layout()

# server = app.server


@app.callback(
    Output("blog-articles-dropdown", "options"),
    Output("blog-articles-dropdown", "value"),
    Input("blog-radio", "value"),
)
def get_article(blog):
    path_article_dir = Path(f"data/data_warehouse/{blog}/articles")
    file_list = os.listdir(path_article_dir)
    articles = []

    for file_name in file_list:
        file_path = path_article_dir / file_name
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                published = data.get("published", "Key 'published' not found in JSON file")
                title = data.get("title", "Key 'title' not found in JSON file")
                articles.append((title, published))
        except json.JSONDecodeError:
            return "Error decoding JSON"

    articles = sorted(articles, key=lambda x: x[1], reverse=True)[:15]
    file_list = [article[1] + ": " + article[0] for article in articles]

    # most recent article set as default value
    return file_list, file_list[0]


@app.callback(
    Output("blog-post", "children"),
    Output("link-to-blog-post", "children"),
    Input("blog-radio", "value"),
    Input("blog-articles-dropdown", "value"),
    Input("prompt-radio", "value"),
    Input("model-radio", "value"),
)
def summarize_article(blog, article, sum_type, model):
    if not article:
        return "No article specified.", ""

    article = f'{article.replace(" ", "_")}.json'  # get file name from title

    if model == "api":
        path_summary_dir = Path(f"data/data_warehouse/{blog}/summarized_articles/{sum_type}")
    else:
        path_summary_dir = Path(f"data/data_warehouse/{blog}/summarized_articles/{model}")

    filename_summary = "Summary_of_" + article
    path_summary_file = path_summary_dir / filename_summary

    # Check if file exists
    if not path_summary_file.exists():
        return f"File {path_summary_file} does not exist.", ""

    try:
        with open(str(path_summary_file), "r") as f:  # Convert Path to str for compatibility
            data = json.load(f)
            summary_content = data.get("text", "Key 'text' not found in JSON file.")
    except json.JSONDecodeError:
        return "Error decoding JSON.", ""

    path_article_dir = Path(f"data/data_warehouse/{blog}/articles")
    path_article_file = path_article_dir / article

    try:
        with open(str(path_article_file), "r") as f:
            data = json.load(f)
            link_to_article = "\nRead more: " + data.get(
                "link", "Key 'link' not found in JSON file"
            )
    except json.JSONDecodeError:
        return "Error decoding JSON", ""

    return summary_content, link_to_article


if __name__ == "__main__":
    app.run_server(port=9000, debug=True)
