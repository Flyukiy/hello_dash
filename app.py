from turtle import width
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go

from dash import html, dcc, dash_table, no_update, Dash
from dash.dependencies import Input, Output
import pandas as pd

app = Dash(__name__)
df = pd.read_csv('intro_bees.csv')
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

app.layout = html.Div(
    # style = {'backgroundColor': 'black', 'color': 'white', 'margin': '0', 'padding': '0'},
    children = [
            html.Div(
                children = [
                    html.H1(style = {'text-align': 'center'}, children = "Hello Dash"),
                ],
            ),
            dcc.Dropdown(
                id = 'selected_year',
                options = [
                    {'label': '2015', 'value': 2015},
                    {'label': '2016', 'value': 2016},
                    {'label': '2017', 'value': 2017},
                    {'label': '2018', 'value': 2018},
                    {'label': '2019', 'value': 2019},
                ],
                multi = False,
                value = 2015,
                style = {'text-align': 'center', 'width': '100%'},
            ),
            # html.Div(
            #     children = [],
            #     id = 'current_value',
            # ),
            html.Br(),
            html.Div(
                children = [
                    html.Label("Choropleth Chart"),
                    dcc.Graph(id="choropleth_chart", figure = {}),
                    html.Br(),
                    html.Label("Bar Chart"),
                    dcc.Graph(id="bar_chart", figure = {}),
                    html.Br(),
                    html.Label("Line Chart"),
                    dcc.Graph(id="line_chart", figure = {}),
                ],
            ),
        ],
)

@app.callback(
    [   
        # Output(component_id="current_value", component_property="children"),
        Output(component_id="choropleth_chart", component_property="figure"),
        Output(component_id="bar_chart", component_property="figure"),
        Output(component_id="line_chart", component_property="figure"),
    ],
    [Input(component_id="selected_year", component_property="value")],
)
def update_figure(option_selected):
    print(f'option_selected: {option_selected}')
    print(type(option_selected))

    # selected_headline = f'User has selected values for {option_selected}'

    dff = df.copy()
    dff = dff[dff["Year"] == option_selected]
    # dff = dff[dff["Affected by"] == "Varroa_mites"]
    
    choropleth_chart = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlGnBu,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark',
    )

    bar_chart = px.bar(
        data_frame=dff,
        x='State',
        y='Pct of Colonies Impacted',
        color_continuous_scale=px.colors.sequential.YlGnBu,
        template='plotly_dark',
    )

    line_chart = px.line(
        data_frame=dff,
        x='State',
        y='Pct of Colonies Impacted',
        template='plotly_dark',
        color='Affected by',
    )

    return choropleth_chart, bar_chart, line_chart

if __name__ == '__main__':
    app.run_server(debug=True)