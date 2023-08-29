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
    Input("blog-radio", "value"),
    Input("blog-articles-dropdown", "value"),
)
# def summarize_article(ix, blog):
def summarize_article(blog, article):
    if article:
        path_article_dir = Path(f"data/data_warehouse/{blog}/articles")
        file_list = os.listdir(path_article_dir)
        file_path = path_article_dir / article
        return summarize.summarize_text(file_path)


if __name__ == "__main__":
    app.run_server(port=9000, debug=True)
