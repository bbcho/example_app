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

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [
        dcc.Checklist(
            id="toggle-rangeslider",
            options=[{"label": "Include Rangeslider", "value": "slider"}],
            value=[None],
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
    ]
)


@app.callback(
    Output("graph", "figure"),
    [
        Input("toggle-rangeslider", "value"),
        Input("dd_code", "value"),
        Input("dd_int", "value"),
        Input("dd_period", "value"),
    ],
)
def display_candlestick(value, cd, interval, period):
    df = yf.download(cd, period=period, interval=interval)

    if (df.shape[0] == 0) & (period == "1d"):
        fig = go.Figure()
        fig.update_layout(
            title="Markets are closed for today, please choose 5d or greater for your period"
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
            title=f"{cd} {interval} Intervals",
        )

    return fig


if __name__ == "__main__":
    app.run_server(debug=False)  # , host='0.0.0.0' port=8000,
