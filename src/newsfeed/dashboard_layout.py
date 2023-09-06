from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html


class LayoutHandler:
    def __init__(self):
        self._blog_options = {"mit": "MIT", "aws": "AWS"}
        self._prompt_options = {"tech": "Technical", "ntech": "Non-technical", "swe": "Svenska"}
        self._model_options = {"api": "GPT-3.5 (API)", "gpt2": "GPT-2 (local)", "t5": "T5 (local)"}

    def create_layout(self):
        return dbc.Container(
            [
                dbc.Card(dbc.CardBody(html.H1("Blog post summary"))),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            children=[
                                dbc.Row(dcc.Markdown(id="blog-post")),
                                dbc.Row(dcc.Markdown(id="link-to-blog-post")),
                            ]
                        ),
                        dbc.Col(
                            children=[
                                dbc.Row(html.P("Choose model:"), className="mt-1"),
                                dbc.Row(
                                    dcc.RadioItems(
                                        id="model-radio",
                                        options=self._model_options,
                                        value="api",
                                    )
                                ),
                                dbc.Row(html.P("")),
                                dbc.Row(html.P("Choose type of summary:"), className="mt-1"),
                                dbc.Row(
                                    dcc.RadioItems(
                                        id="prompt-radio",
                                        options=self._prompt_options,
                                        value="tech",
                                    )
                                ),
                                dbc.Row(html.P("")),
                                dbc.Row(html.P("Choose blog:"), className="mt-1"),
                                dbc.Row(
                                    dcc.RadioItems(
                                        id="blog-radio",
                                        options=self._blog_options,
                                        value="mit",
                                    )
                                ),
                                dbc.Row(html.P("")),
                                dbc.Row(html.P("Choose article"), className="mt-1"),
                                dbc.Row(
                                    dcc.Dropdown(
                                        id="blog-articles-dropdown",
                                        options=[],
                                        style={"width": "100&", "font-size": "1em"},
                                        searchable=True,
                                    )
                                ),
                            ]
                        ),
                    ],
                ),
            ]
        )
