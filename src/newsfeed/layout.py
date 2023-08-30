from pathlib import Path

import dash_bootstrap_components as dbc
from dash import dcc, html


class Layout:
    def __init__(self):
        self._blog_options = {"mit": "MIT"}
        self._prompt_options = {"tech": "Technical", "nontech": "Non-technical"}

    def layout(self):
        return dbc.Container(
            [
                dbc.Card(dbc.CardBody(html.H1("Blog post summary"))),
                dbc.Row(
                    className="mt-4",
                    children=[
                        dbc.Col(dcc.Markdown(id="blog-post")),
                        dbc.Col(
                            children=[
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
                                    )
                                ),
                            ]
                        ),
                    ],
                ),
            ]
        )
