# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import numpy as np
import plotly.express as px

# Incorporate data
X = pd.read_csv('X.csv')
y = pd.read_csv('y.csv')
df = pd.read_csv('df.csv')

# Precomputed summaries
price_summary = df['Price'].describe().reset_index()

# Ensure 'Year-Month' is in datetime format for correlation calculation
X['Year-Month'] = pd.to_datetime(X['Year-Month'], format='%Y-%m', errors='coerce')

# Drop non-numeric columns before calculating the correlation matrix
corr_matrix = X.select_dtypes(include=[np.number]).corr()

# Calculate the percentage increase from the previous month's price
latest_price = y.iloc[-1]
previous_price = y.iloc[-2]
percent_increase = (((latest_price - previous_price) / previous_price) * 100).iloc[0]

# Initialize the app
app = Dash()
server = app.server

# App layout
app.layout = html.Div([
    html.Div('📊 Predicting Egg Prices', style={'textAlign': 'center', 'color': 'black', 'fontSize': 50, 'marginBottom': '20px'}),

    # Top row: Summary Cards
    html.Div([
        html.Div([
            html.H5('Latest Price', style={'textAlign': 'center'}),
            html.Div(f"${df['Price'].iloc[-1]:,.2f}", style={'textAlign': 'center', 'fontSize': 30, 'color': 'green'}),
            html.Small(f"↑ {percent_increase:.2f}% from last month", style={'display': 'block', 'textAlign': 'center', 'color': 'green'})
        ], style={'width': '30%', 'padding': '20px', 'border': '1px solid lightgray', 'borderRadius': '10px', 'margin': '10px'}),

        html.Div([
            html.H5('Total Records', style={'textAlign': 'center'}),
            html.Div(f"{len(df)}", style={'textAlign': 'center', 'fontSize': 30, 'color': 'purple'}),
        ], style={'width': '30%', 'padding': '20px', 'border': '1px solid lightgray', 'borderRadius': '10px', 'margin': '10px'}),

        html.Div([
            html.H5('Price Range', style={'textAlign': 'center'}),
            html.Div(f"${df['Price'].min():.0f} - ${df['Price'].max():.0f}", style={'textAlign': 'center', 'fontSize': 30, 'color': 'orange'}),
        ], style={'width': '30%', 'padding': '20px', 'border': '1px solid lightgray', 'borderRadius': '10px', 'margin': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    # Second row: Tables (X, y, and Price Summary)
    html.Div([
        html.Div([
            html.H4('X Data'),
            dash_table.DataTable(
                data=X.to_dict('records'),
                columns=[{"name": i, "id": i} for i in X.columns],
                page_size=5,
                style_table={'overflowX': 'auto'}
            )
        ], style={'width': '30%', 'padding': '10px'}),

        html.Div([
            html.H4('y Data'),
            dash_table.DataTable(
                data=y.to_dict('records'),
                columns=[{"name": i, "id": i} for i in y.columns],
                page_size=5,
                style_table={'overflowX': 'auto'}
            )
        ], style={'width': '30%', 'padding': '10px'}),

        html.Div([
            html.H4('Price Summary'),
            dash_table.DataTable(
                data=price_summary.to_dict('records'),
                columns=[{"name": i, "id": i} for i in price_summary.columns],
                style_table={'overflowX': 'auto'},
                page_size=6
            )
        ], style={'width': '30%', 'padding': '10px'}),
    ], style={'display': 'flex'}),

    # Third row: Download buttons
    html.Div([
        html.Div([
            html.Button("Download X Data (CSV)", id="btn-download-x"),
            dcc.Download(id="download-x")
        ], style={'width': '30%', 'padding': '30px'}),

        html.Div([
            html.Button("Download y Data (CSV)", id="btn-download-y"),
            dcc.Download(id="download-y")
        ], style={'width': '30%', 'padding': '30px'}),
    ], style={'display': 'flex'}),

    # Fourth Row: Line Plot
    html.Div([
        html.Div([
            html.H4('Price Trend (Line Plot)'),
            dcc.Graph(figure=px.line(df, x='Year-Month', y='Price', markers=True))
        ], style={'width': '100%', 'padding': '10px'}),
    ], style={'display': 'flex', 'marginTop': '20px'}),

    # Fifth row: Histograms and Correlation
    html.Div([
        html.Div([
            html.H4('Price Distribution (Histogram)'),
            dcc.Graph(figure=px.histogram(df, x='Price', nbins=10))
        ], style={'width': '50%', 'padding': '10px'}),

        html.Div([
            html.H4('Feature Correlations (Heatmap)'),
            dcc.Graph(
                figure=px.imshow(
                    corr_matrix,
                    text_auto=True,
                    color_continuous_scale='Blues',
                    title='Correlation Matrix'
                )
            )
        ], style={'width': '50%', 'padding': '10px'}),
    ], style={'display': 'flex', 'marginTop': '20px'}),

], style={'padding': '20px'})

from dash.dependencies import Input, Output
import base64
import io

@app.callback(
    Output("download-x", "data"),
    Input("btn-download-x", "n_clicks"),
    prevent_initial_call=True,
)
def download_x(n_clicks):
    return dcc.send_data_frame(X.to_csv, "X.csv", index=False)

@app.callback(
    Output("download-y", "data"),
    Input("btn-download-y", "n_clicks"),
    prevent_initial_call=True,
)
def download_y(n_clicks):
    return dcc.send_data_frame(y.to_csv, "y.csv", index=False)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
