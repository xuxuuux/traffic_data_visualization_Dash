# traffic_data_visualization_Dash

A simple interactive dashboard built with Dash and Plotly to visualize simulated traffic data.

## Simulated traffic data

The traffic data in this project is simulated using a Python script.
 It models traffic conditions for five road segments: **A, B, C, D, and E**.

1.  During **peak hours (7–9 AM and 5–7 PM)**, the vehicle count is higher and the average speed is lower.
2.  During **off-peak hours (10 AM–4 PM and after 8 PM)**, the traffic volume decreases and vehicles move faster.
3.  In addition, random noise is introduced to make the data more realistic.

```python
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
```

## Dash & plotly to show traffic data

**After you run the code**, you can see visit the website: http://127.0.0.1:8050/

1. You can view the traffic conditions for different road segments each day. I used a **line chart** and a **bar chart** to display the data.

2. In addition, you can freely download the charts from the website and save them in **PNG** format.

   <img src="pic\traffic1.png" alt="1" style="zoom:25%;" />

<img src="pic\traffic2.png" alt="1" style="zoom:25%;" />

<img src="pic\traffic3.png" alt="1" style="zoom:25%;" />

