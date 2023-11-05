import plotly.express as px
import pandas as pd

# Data
data = [
    {
        "name": "Monica",
        "steps": 45688,
        "pictureSettings": {
            "src": "https://www.amcharts.com/wp-content/uploads/2019/04/monica.jpg",
        },
    },
    {
        "name": "Joey",
        "steps": 35781,
        "pictureSettings": {
            "src": "https://www.amcharts.com/wp-content/uploads/2019/04/joey.jpg",
        },
    },
    {
        "name": "Ross",
        "steps": 25464,
        "pictureSettings": {
            "src": "https://www.amcharts.com/wp-content/uploads/2019/04/ross.jpg",
        },
    },
    {
        "name": "Phoebe",
        "steps": 18788,
        "pictureSettings": {
            "src": "https://www.amcharts.com/wp-content/uploads/2019/04/phoebe.jpg",
        },
    },
    {
        "name": "Rachel",
        "steps": 15465,
        "pictureSettings": {
            "src": "https://www.amcharts.com/wp-content/uploads/2019/04/rachel.jpg",
        },
    },
    {
        "name": "Chandler",
        "steps": 11561,
        "pictureSettings": {
            "src": "https://www.amcharts.com/wp-content/uploads/2019/04/chandler.jpg",
        },
    },
]

# Create a DataFrame
df = pd.DataFrame(data)

# Create the chart using Plotly Express
fig = px.bar(
    df,
    x="steps",
    y="name",
    text="steps",
    labels={"steps": "Income"},
    title="Friends' Income",
    template="plotly",
)

# Customize the appearance
fig.update_traces(
    texttemplate="%{text:.0f}",
    marker=dict(line=dict(width=0)),
    hoverinfo="x+y",
)

# Show the chart
fig.show()
