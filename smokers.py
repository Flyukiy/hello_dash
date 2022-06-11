from turtle import width
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go

from dash import html, dcc, dash_table, no_update, Dash
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]

load_figure_template(templates)
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY, dbc_css],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)



df = pd.read_csv('smokers.csv')
# df = df[df["type"] == "Smoking"]
df.reset_index(inplace=True)
print(df[:5])

app.layout = dbc.Container(
    fluid="md",
    className="dbc",
    children = [
        html.Br(),
        html.Div(
            className="",
            children = [
                html.H2(style = {'text-align': 'center'}, children = "Smoking and Drinking data (20 years old and over)"),
                html.H3(style = {'text-align': 'center'}, children = "South Korea, 2014"),
            ],
        ),
        html.Br(),
        html.P("Filter"),
        dcc.Dropdown(
            id = 'types',
            options = [
                {'label': 'Smokers', 'value': 'Smokers'},
                {'label': 'Non smoker', 'value': 'Non smoker'},
                {'label': 'Quit smoking', 'value': 'Quit smoking'},
                {'label': 'Never smoked', 'value': 'Never smoked'},
            ],
            multi = False,
            value = 'Smokers',
            style = {'text-align': 'center', 'width': '100%'},
        ),
        # html.Div(
        #     children = [],
        #     id = 'current_value',
        # ),
        html.Br(),
        html.Div(
            children = [
                html.P("Bar Chart"),
                dcc.Graph(id="bar_chart", figure = {}),
                html.Br(),
                html.P("Line Chart"),
                dcc.Graph(id="line_chart", figure = {}),
            ],
        ),
    ],
)

@app.callback(
    [
        Output(component_id="bar_chart", component_property="figure"),
        Output(component_id="line_chart", component_property="figure"),
    ],
    [Input(component_id="types", component_property="value")],
)
def update_graph(type):
    dff = df.copy()
    dff = dff[dff["type"] != "Total"]
    # dff = dff[dff["filter"] == type]
    dff.reset_index(inplace=True)
    print(dff[:5])
    fig_bar = px.bar(
        data_frame=dff,
        x=[
            "filter", "Less than once per month", "2-3 per month", "1-2 times per week",
            "2-4 times per week", "Everyday", "No drinking", "Quiter", "Never"
        ],
        y="filter",
        color="filter",
        barmode="group",
        template="cyborg",
    )
    fig_line = px.line(
        data_frame=dff,
        x="Drinking",
        y=[
            "Less than once per month", "2-3 per month", "1-2 times per week",
            "2-4 times per week", "Everyday", "No drinking", "Quiter", "Never"
        ],
        markers = True,
        color="filter",
        template="cyborg",
    )
    return fig_bar, fig_line

if __name__ == '__main__':
    app.run_server(debug=True)