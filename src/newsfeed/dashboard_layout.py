from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html


class LayoutHandler:
    def __init__(self):
        self._blog_options = {"mit": "MIT", "aws": "AWS", "openai": "OpenAI"}
        self._prompt_options = {"tech": "Technical", "ntech": "Non-technical", "swe": "Svenska"}
        self._model_options = {"api": "GPT-3.5 (API)", "gpt2": "GPT-2 (local)", "t5": "T5 (local)"}

    def create_layout(self):
        return dbc.Container(
            [
                dbc.Row(
                    html.H1("Essentify"),
                    style={"text-align": "center"},
                    className="mt-3",
                ),
                dbc.Row(
                    html.H3("Blog Summary Dashboard"),
                    style={"text-align": "center"},
                    className="mt-1",
                ),
                dbc.Row(
                    className="mt-5",
                    children=[
                        dbc.Col(html.H4("Blog"), className="mt-1"),
                        dbc.Col(html.H4("Summary Type"), className="mt-1"),
                        dbc.Col(html.H4("Model"), className="mt-1"),
                    ],
                ),
                dbc.Row(
                    className="mt-0",
                    children=[
                        dbc.Col(
                            dcc.RadioItems(
                                id="blog-radio",
                                options=self._blog_options,
                                value="mit",
                                style={"display": "flex", "flex-direction": "column"},
                                inputStyle={"margin-right": "10px"},
                            )
                        ),
                        dbc.Col(
                            dcc.RadioItems(
                                id="prompt-radio",
                                options=self._prompt_options,
                                value="tech",
                                style={"display": "flex", "flex-direction": "column"},
                                inputStyle={"margin-right": "10px"},
                            )
                        ),
                        dbc.Col(
                            dcc.RadioItems(
                                id="model-radio",
                                options=self._model_options,
                                value="api",
                                style={"display": "flex", "flex-direction": "column"},
                                inputStyle={"margin-right": "10px"},
                            )
                        ),
                    ],
                ),
                dbc.Row(html.H5("Article"), className="mt-5"),
                dbc.Row(
                    dcc.Dropdown(
                        id="blog-articles-dropdown",
                        options=[],
                        style={"width": "100&", "font-size": "1em"},
                        searchable=True,
                    )
                ),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(
                            children=[
                                dbc.Row(dcc.Markdown(id="blog-post")),
                                dbc.Row(dcc.Markdown(id="link-to-blog-post")),
                            ]
                        ),
                    ],
                ),
            ]
        )
