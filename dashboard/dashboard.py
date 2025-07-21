from datetime import datetime
import time
from dash import Dash, html, dcc, Output, Input
import plotly.graph_objs as go
import threading
import os

# Store live data and default thresholds
data_buffer = {
    'time': [],
    'cpu': [],
    'mem': [],
    'disk': [],
    'net': [],
    'load': []
}

thresholds = {
    'cpu': 75,
    'mem': 75,
    'disk': 75,
    'net': 500,
    'load': 2
}

metrics = ['cpu', 'mem', 'disk', 'net', 'load']
metric_names = {
    'cpu': "CPU Usage (%)",
    'mem': "Memory Usage (%)",
    'disk': "Disk Usage (%)",
    'net': "Network Traffic (MB)",
    'load': "System Load"
}

# Function to read the named pipe
def pipe_reader():
    pipe_path = "/tmp/sysmetrics.pipe"
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)

    while True:
        try:
            with open(pipe_path, 'r') as pipe:
                line = pipe.readline().strip()
                if line:
                    parts = {k.strip(): float(v.strip().replace('%', '').replace('MB', ''))
                             for k, v in (item.split(":") for item in line.split("|"))}
                    timestamp = time.strftime("%H:%M:%S")
                    data_buffer['time'].append(timestamp)
                    for key in ['cpu', 'mem', 'disk', 'net', 'load']:
                        data_buffer[key].append(parts.get(key.upper(), 0))
                        if len(data_buffer[key]) > 20:
                            data_buffer[key].pop(0)
                    if len(data_buffer['time']) > 20:
                        data_buffer['time'].pop(0)
        except Exception as e:
            print("Pipe error:", e)
            time.sleep(1)

# Start pipe reading thread
threading.Thread(target=pipe_reader, daemon=True).start()

# Dash app
app = Dash(__name__)
app.title = "System Metrics Dashboard"

app.layout = html.Div(style={'backgroundColor': '#1e1e1e', 'color': 'white', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.H1("System Performance Dashboard", style={'marginBottom': '1rem'}),
    
    dcc.Dropdown(
        id='metric-dropdown',
        options=[{'label': metric_names[m], 'value': m} for m in metrics] + [{'label': "All Metrics", 'value': 'all'}],
        value='cpu',
        style={'width': '300px', 'color': 'black'}
    ),

    html.Div(id='threshold-sliders', children=[]),
    
    html.Div(id='alert-banner', style={'color': 'white', 'padding': '10px', 'marginBottom': '1rem'}),
    
    dcc.Graph(id='live-graph'),
    
    dcc.Interval(id='interval-update', interval=5000, n_intervals=0)
])

# Sliders for thresholds
@app.callback(
    Output('threshold-sliders', 'children'),
    Input('metric-dropdown', 'value')
)
def update_sliders(selected_metric):
    if selected_metric == 'all':
        return [html.Div([
            html.Label(f"{metric_names[m]} Threshold:"),
            dcc.Slider(id=f'slider-{m}', min=0, max=1000 if m == 'net' else 100, step=1, value=thresholds[m],
                       marks={0: '0', 1000 if m == 'net' else 100: 'Max'}, tooltip={"placement": "bottom"})
        ], style={'marginBottom': '1rem'}) for m in metrics]
    else:
        return html.Div([
            html.Label(f"{metric_names[selected_metric]} Threshold:"),
            dcc.Slider(id=f'slider-{selected_metric}', min=0, max=1000 if selected_metric == 'net' else 100, step=1,
                       value=thresholds[selected_metric],
                       marks={0: '0', 1000 if selected_metric == 'net' else 100: 'Max'}, tooltip={"placement": "bottom"})
        ], style={'marginBottom': '1rem'})

# Main update callback
@app.callback(
    Output('live-graph', 'figure'),
    Output('alert-banner', 'children'),
    Input('interval-update', 'n_intervals'),
    Input('metric-dropdown', 'value'),
    *[Input(f'slider-{m}', 'value') for m in metrics]
)
def update_graph(n, selected_metric, *slider_values):
    for i, m in enumerate(metrics):
        thresholds[m] = slider_values[i]

    alert_msgs = []

    fig = go.Figure()

    colors = {
        'cpu': 'cyan',
        'mem': 'orange',
        'disk': 'lime',
        'net': 'magenta',
        'load': 'yellow'
    }

    if selected_metric == 'all':
        for m in metrics:
            fig.add_trace(go.Scatter(
                x=data_buffer['time'],
                y=data_buffer[m],
                mode='lines+markers',
                name=metric_names[m],
                line=dict(color=colors[m])
            ))
            fig.add_trace(go.Scatter(
                x=data_buffer['time'],
                y=[thresholds[m]] * len(data_buffer['time']),
                mode='lines',
                name=f"{metric_names[m]} Threshold",
                line=dict(dash='dash', color='red')
            ))
            if data_buffer[m] and data_buffer[m][-1] > thresholds[m]:
                alert_msgs.append(f"⚠️ {metric_names[m]} is above threshold: {data_buffer[m][-1]:.2f} > {thresholds[m]}")
    else:
        m = selected_metric
        fig.add_trace(go.Scatter(
            x=data_buffer['time'],
            y=data_buffer[m],
            mode='lines+markers',
            name=metric_names[m],
            line=dict(color=colors[m])
        ))
        fig.add_trace(go.Scatter(
            x=data_buffer['time'],
            y=[thresholds[m]] * len(data_buffer['time']),
            mode='lines',
            name="Threshold",
            line=dict(dash='dash', color='red')
        ))
        if data_buffer[m] and data_buffer[m][-1] > thresholds[m]:
            alert_msgs.append(f"⚠️ {metric_names[m]} is above threshold: {data_buffer[m][-1]:.2f} > {thresholds[m]}")

    fig.update_layout(
        paper_bgcolor='#1e1e1e',
        plot_bgcolor='#2e2e2e',
        font=dict(color='white'),
        xaxis_title="Time",
        yaxis_title="Value",
        margin=dict(t=40, r=10, l=10, b=40)
    )

    banner = html.Div([
        html.Strong("Alerts:"),
        html.Ul([html.Li(msg) for msg in alert_msgs])
    ]) if alert_msgs else ""

    return fig, banner

app.run(host="0.0.0.0", port=8050)
