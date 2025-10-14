import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# 加载数据
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 参数设置
segments = ["A", "B", "C", "D", "E"]
start_time = datetime(2025, 10, 13, 6, 0)
end_time = datetime(2025, 10, 13, 22, 0)
time_range = pd.date_range(start=start_time, end=end_time, freq="H")

data = []

np.random.seed(42)

for seg in segments:
    # The base speeds for different sections of the road
    base_speed = {
        "A": 45,
        "B": 55,
        "C": 35,
        "D": 50,
        "E": 60
    }[seg]

    for t in time_range:
        hour = t.hour

        # Simulate the peak and off-peak traffic flow of vehicles
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            count = np.random.randint(180, 260)
            speed = base_speed - np.random.randint(8, 15)
        elif 10 <= hour <= 16:
            count = np.random.randint(100, 160)
            speed = base_speed - np.random.randint(2, 6)
        else:
            count = np.random.randint(60, 120)
            speed = base_speed + np.random.randint(2, 8)

        # 加入随机微调
        count += np.random.randint(-10, 10)
        speed += np.random.normal(0, 2)

        data.append({
            "time": t,
            "segment": seg,
            "vehicle_count": max(count, 0),
            "avg_speed": max(speed, 5)
        })

df = pd.DataFrame(data)
df.to_csv("traffic_sample.csv", index=False)

# df = pd.read_csv("traffic_sample.txt", sep=",")
# 保存为csv
df.to_csv("traffic_sample.csv", index=False)

df = pd.read_csv("traffic_sample.csv")
df['time'] = pd.to_datetime(df['time'])

# 初始化应用
app = dash.Dash(__name__)

# 页面布局
app.layout = html.Div([
    html.H2("Traffic Flow Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Road Segment:"),
        dcc.Dropdown(
            id='segment-dropdown',
            options=[{'label': seg, 'value': seg} for seg in df['segment'].unique()],
            value='A'
        ),
    ], style={'width': '40%', 'margin': 'auto'}),

    dcc.Graph(id='speed-graph'),
    dcc.Graph(id='count-graph'),

    html.Div("Data Source: Synthetic traffic data for demo purposes",
             style={'textAlign': 'center', 'fontSize': '12px', 'color': 'gray'})
])

# Callback function: Update the chart based on the selection.
@app.callback(
    [Output('speed-graph', 'figure'),
     Output('count-graph', 'figure')],
    [Input('segment-dropdown', 'value')]
)
def update_graphs(selected_segment):
    dff = df[df['segment'] == selected_segment]

    fig_speed = px.line(
        dff, x='time', y='avg_speed', title=f"Average Speed over Time – Segment {selected_segment}",
        markers=True
    )
    fig_speed.update_layout(yaxis_title="Speed (km/h)", template="plotly_white")

    fig_count = px.bar(
        dff, x='time', y='vehicle_count', title=f"Vehicle Count – Segment {selected_segment}",
    )
    fig_count.update_layout(yaxis_title="Vehicles", template="plotly_white")

    return fig_speed, fig_count

if __name__ == "__main__":
    app.run_server(debug=True)
