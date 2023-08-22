

import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Define the list of stock tickers
tickers = ['^NSEI']

# Define the start and end dates
start_date = '2000-01-01'
end_date = '2023-12-12'


ticker_data = pd.DataFrame()
for ticker in tickers:
    ticker_df = yf.download(ticker, start=start_date, end=end_date)
    ticker_df['Ticker'] = ticker
    ticker_data = pd.concat([ticker_data, ticker_df])


sma_days = 50
ticker_data['SMA'] = ticker_data.groupby('Ticker')['Close'].rolling(window=sma_days).mean().reset_index(0, drop=True)

# Create a plot for each ticker and its SMA
data = []
for ticker in tickers:
    ticker_df = ticker_data.loc[ticker_data['Ticker'] == ticker]
    trace_stock_price = go.Scatter(x=ticker_df.index, y=ticker_df['Close'], name=ticker)
    trace_sma = go.Scatter(x=ticker_df.index, y=ticker_df['SMA'], name=ticker + ' SMA')
    data.append(trace_stock_price)
    data.append(trace_sma)


layout = go.Layout(title='Stock Prices and SMA - 5 Year Period',
                   xaxis=dict(title='Date'),
                   yaxis=dict(title='Price'))

# Create the plot using Plotly
fig = go.Figure(data=data, layout=layout)
fig.show()

# Stock Stanard Deviations 

tickers = ['^NSEI']
start_date = '2015-01-01'
end_date = '2023-12-30'


ticker_data = {}
for ticker in tickers:
    ticker_df = yf.download(ticker, start=start_date, end=end_date)
    ticker_data[ticker] = ticker_df


# Buy Timing

for ticker in tickers:
    std = ticker_data[ticker]['Close'].std()
    avg_price = ticker_data[ticker]['Close'].mean()
    buy_price = avg_price - std
    current_price = ticker_data[ticker]['Close'].iloc[-1]
    if current_price > buy_price:
        print(ticker + ' - Don\'t Buy')
    else:
        print(ticker + ' - Buy')

    print('Current price: ' + str(round(current_price, 2)) + ', Buy price: ' + str(round(buy_price, 2)))
    print(std)
    print('-------------------')


# Sell Timing

for ticker in tickers:
    std = ticker_data[ticker]['Close'].std()
    avg_price = ticker_data[ticker]['Close'].mean()
    buy_price = avg_price + std
    current_price = ticker_data[ticker]['Close'].iloc[-1]
    if current_price > buy_price:
        print(ticker + ' - Sell')
    else:
        print(ticker + ' - Do not sell')

    print('Current price: ' + str(round(current_price, 2)) + ', Sell price: ' + str(round(buy_price, 2)))
    print(std, avg_price)
    print('-------------------')


