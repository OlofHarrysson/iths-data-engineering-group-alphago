import json
import os
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

from newsfeed import layout, summarize

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
    # makes responsivity possible (different web browser sizes)
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
    # suppress_callback_exceptions=True
)

app.layout = layout.Layout().layout()

# server = app.server


@app.callback(
    Output("blog-articles-dropdown", "options"),
    Input("blog-radio", "value"),
)
def get_article(blog):
    path_article_dir = Path(f"data/data_warehouse/{blog}/articles")
    file_list = os.listdir(path_article_dir)
    return file_list


@app.callback(
    Output("blog-post", "children"),
    Output("link-to-blog-post", "children"),
    Input("blog-radio", "value"),
    Input("blog-articles-dropdown", "value"),
)
def summarize_article(blog, article):
    if not article:
        return "No article specified."

    path_summary_dir = Path(f"data/data_warehouse/{blog}/summarized_articles")

    # Check if directory exists
    if not path_summary_dir.exists():
        return f"Directory {path_summary_dir} does not exist."

    filename_summary = "Summary_of_" + article
    path_summary_file = path_summary_dir / filename_summary

    # Check if file exists
    if not path_summary_file.exists():
        return f"File {path_summary_file} does not exist."

    try:
        with open(str(path_summary_file), "r") as f:  # Convert Path to str for compatibility
            data = json.load(f)
            summary_content = data.get("text", "Key 'text' not found in JSON file.")
    except json.JSONDecodeError:
        return "Error decoding JSON."

    path_article_dir = Path(f"data/data_warehouse/{blog}/articles")
    path_article_file = path_article_dir / article

    try:
        with open(str(path_article_file), "r") as f:
            data = json.load(f)
            link_to_article = "Read more: " + data.get("link", "Key 'link' not found in JSON file")
    except json.JSONDecodeError:
        return "Error decoding JSON", None

    return summary_content, link_to_article


if __name__ == "__main__":
    app.run_server(port=9000, debug=True)
