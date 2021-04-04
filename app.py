import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import flask

# import pandas_datareader.data as web

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

interval = "5m"
period = "5d"
cd = "CL=F"
refresh_int = 10  # number of seconds between refreshes

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

server = flask.Flask(__name__)

# n_int = 5 * 60 * 1000  # how often to update chart

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [
        dcc.Checklist(
            id="toggle-rangeslider",
            options=[{"label": "Include Rangeslider", "value": "slider"}],
            value="slider",  # [None] to turn off by default
        ),
        
        dcc.Dropdown(
            id="dd_code",
            options=[
                {"label": "CL<0>", "value": "CL=F"},
                {"label": "RB<0>", "value": "RB=F"},
                {"label": "HO<0>", "value": "HO=F"},
            ],
            value="CL=F",
        ),
        dcc.Dropdown(
            id="dd_int",
            options=[
                {"label": "1m", "value": "1m"},
                {"label": "5m", "value": "5m"},
                {"label": "15m", "value": "15m"},
            ],
            value="5m",
        ),
        dcc.Dropdown(
            id="dd_period",
            options=[
                {"label": "1d", "value": "1d"},
                {"label": "5d", "value": "5d"},
                {"label": "1mo", "value": "1mo"},
            ],
            value="5d",
        ),
        dcc.Graph(id="graph"),
        dcc.Interval(
            id="interval-component",
            interval=refresh_int * 1000,  # in milliseconds
            n_intervals=0,
        ),
    ]
)


@app.callback(
    Output("graph", "figure"),
    [
        Input("toggle-rangeslider", "value"),
        Input("dd_code", "value"),
        Input("dd_int", "value"),
        Input("dd_period", "value"),
        Input("interval-component", "n_intervals"),
    ],
)
def display_candlestick(value, cd, interval, period, n):
    print(cd)
    df = yf.download(cd, period=period, interval=interval)
    last_update = pd.Timestamp.now()

    if (df.shape[0] == 0) & (period == "1d"):
        fig = go.Figure()
        fig.update_layout(
            title="Markets are closed for today, please choose 5d or greater for your period",
        )
    else:
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                )
            ]
        )
        # fig.update_layout(xaxis_rangeslider_visible=False)

        fig.update_layout(
            xaxis_rangeslider_visible="slider" in value,
            title=f"{cd} {interval} Intervals. Last updated {last_update}, {n} updates",
        )

    fig.update_layout(
        uirevision=f"{cd} {period} {interval}"  # makes sure that the zoom levels, etc... are not reset when data updates. List or tuple doesn't work
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)  # , host='0.0.0.0' port=8000,
