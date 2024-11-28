import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go



ticker = 'AAPL'
data = yf.download(tickers=ticker, period='1d', interval='1m')

print(data.tail())




app = dash.Dash(__name__)


def fetch_stock_data(symbol):
    data = yf.download(tickers=symbol, period='1d', interval='1m')
    return data


app.layout = html.Div([
    dcc.Dropdown(
        id='stock-picker',
        options=[
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Google', 'value': 'GOOG'},
            {'label': 'Tesla', 'value': 'TSLA'}
        ],
        value='AAPL'  
    ),
    dcc.Graph(id='stock-graph'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000, 
        n_intervals=0
    )
])


@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-picker', 'value'), Input('interval-component', 'n_intervals')]
)
def update_graph(stock_ticker, n):
    
    data = fetch_stock_data(stock_ticker)
    
   
    figure = go.Figure(
        data=[
            go.Scatter(
                x=data.index, 
                y=data['Close'], 
                mode='lines',
                name=stock_ticker
            )
        ]
    )
    
    
    figure.update_layout(
        title=f"Real-Time Stock Price: {stock_ticker}",
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        plot_bgcolor='rgb(230, 230, 250)',
        paper_bgcolor='rgb(245, 245, 245)'
    )
    
    return figure


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
