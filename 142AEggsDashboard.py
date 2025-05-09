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
    html.Div('📊 Dashboard Overview', style={'textAlign': 'center', 'color': 'darkblue', 'fontSize': 36, 'marginBottom': '20px'}),

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

    # Third row: Downloadable CSVs
    html.Div([
        # Download X.csv
        html.Div([
            dcc.Download(id='download-x'),
            html.A('Download X Data', id='download-link-x', href='/download-x', target='_blank')
        ], style={'width': '30%', 'padding': '30px'}),

        # Download y.csv
        html.Div([
            dcc.Download(id='download-y'),
            html.A(
                'Download y Data',
                id='download-link-y',
                href='https://raw.githubusercontent.com/xeniachen-01/142a-eggs/main/y.csv',  # Correct raw file URL
                target='_blank',
                download='y.csv'  # Suggests a filename for the downloaded file
            )
        ], style={'width': '30%', 'padding': '30px'}),

        # Dropdown menu for individual datasets
        html.Div([
            html.H4('Download Individual Datasets'),
            dcc.Dropdown(
                id='dataset-dropdown',
                options=[
                    {'label': 'Avian Influenza', 'value': 'americas-outbreaks.csv'},
                    {'label': 'Dataset 2', 'value': 'dataset2.csv'},
                    {'label': 'Dataset 3', 'value': 'dataset3.csv'}
                ],
                placeholder='Select a dataset',
                style={'width': '80%'}
            ),
            html.Div(id='download-dataset-container', style={'marginTop': '10px'}),
        ], style={'width': '30%', 'padding': '10px'}),
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
# Note: The download links for X and y are placeholders. You may need to implement the download functionality using Flask or another method.