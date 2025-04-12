import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import psutil
import plotly.graph_objs as go
import threading
import time

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Real-Time System Monitoring Dashboard"),
    dcc.Graph(id='live-update-graph', style={'height': '70vh'}),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(id='live-update-text')
])

# Function to collect system metrics
def collect_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    return cpu_usage, memory_usage

# Callback to update the graph and text
@app.callback(
    Output('live-update-graph', 'figure'),
    Output('live-update-text', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    cpu_usage, memory_usage = collect_metrics()
    
    # Create a bar graph for CPU and Memory usage
    figure = {
        'data': [
            go.Bar(x=['CPU Usage', 'Memory Usage'], y=[cpu_usage, memory_usage], marker_color=['blue', 'orange'])
        ],
        'layout': go.Layout(
            title='CPU and Memory Usage',
            yaxis=dict(range=[0, 100]),
            xaxis_title='Metrics',
            yaxis_title='Usage (%)'
        )
    }
    
    # Update text display
    text = f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}%"
    
    return figure, text

# Function to run the Dash app
def run_server():
    app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':
    # Run the server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    
    # Keep the main thread alive
    while True:
        time.sleep(1)
