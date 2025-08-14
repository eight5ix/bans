import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Output, Input

# Read CSV
df = pd.read_csv("C:/Users/kaplant/Downloads/2025-08-13-boulderans.csv")

cols = [
    'Aquatic Plants Attached', 'Standing Water',
    'Dirty Crusty Slimy', 'Animals Found', 'Mussels Found'
]

ndf = df.copy()
for col in cols:
    ndf[col] = ndf[col].str.strip().map({'Yes': 1, 'No': 0}).fillna(-1)

long_ndf = ndf.melt(
    id_vars=['Inspection ID','Registration Number', 'Inspection Date', 'Contact Type'],
    value_vars=cols,
    var_name='Category',
    value_name='Value'
)

fig = px.bar(
    long_ndf,
    x="Category",
    y="Value",
    color="Category",
    barmode="stack",
    hover_data=["Registration Number", "Inspection Date", "Contact Type", "Inspection ID"]
)

fig.update_traces(
    customdata=long_ndf[["Registration Number", "Inspection Date", "Contact Type", "Inspection ID"]],
    hovertemplate="""
    CL: %{customdata[0]}<br>
    Date: %{customdata[1]}<br>
    Type: %{customdata[2]}<br>
    <extra></extra>"""
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Boulder ANS Stacked Bar Chart"),
    html.H3("Click on a block to open inspection in ANS"),
    dcc.Graph(id='bar-chart', figure=fig, style={'cursor': 'pointer'}),
    dcc.Location(id='url', refresh=True)  # for redirecting
])

# Callback to open a new tab when a bar is clicked
@app.callback(
    Output('url', 'href'),
    Input('bar-chart', 'clickData'),
    prevent_initial_call=True
)
def open_link(clickData):
    if clickData is None:
        return dash.no_update
    # Get Inspection ID of clicked bar
    inspection_id = clickData['points'][0]['customdata'][3]
    # Build URL
    url = f"https://watercraftinspection.org/Inspection/Edit/{inspection_id}?pageIndex=0"
    # Open in new tab using JS
    return url

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8051, debug=False)
