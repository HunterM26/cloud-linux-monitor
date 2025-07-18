import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os

PIPE_PATH = "/tmp/sysmetrics.pipe"

app = dash.Dash(__name__)
app.title = "Monitor test"

app.layout = html.Div([
    html.H2("System Metrics Dashboard"),
    html.Div(id='live-metrics', style={'fontSize': 24}),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

@app.callback(Output('live-metrics', 'children'), Input('interval', 'n_intervals'))
def update_metrics(n):
    try:
        with open(PIPE_PATH, 'r') as f:
            return f.readline().strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=False)

