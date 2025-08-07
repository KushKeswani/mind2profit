"""
Generated Strategy: Test Strategy
Description: A test strategy
Generated: 2025-08-05 17:56:37
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API keys
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def fetch_data(symbol, start_date, end_date):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        params = {
            'symbol': symbol,
            'timeframe': '1Min',
            'start': start_date,
            'end': end_date
        }
        response = requests.get(base_url + 'stocks/' + symbol + '/bars', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(risk_percent, current_price, stop_loss_pct):
    try:
        risk_amount = risk_percent * 10000  # Assuming $10,000 portfolio
        position_size = risk_amount / (current_price * stop_loss_pct)
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    risk_per_trade = 0.01
    
    df = fetch_data(symbol, start_date, end_date)
    if df is None:
        return
    
    # Add indicators
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['macd'] = ta.trend.MACD(df['close'], window_slow=26, window_fast=12).macd()
    df['macd_signal'] = ta.trend.MACD(df['close'], window_slow=26, window_fast=12).macd_signal()
    df['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma()
    df['sma_50'] = ta.trend.SMAIndicator(df['close'], window=50).sma()
    
    trades = []
    position_size = 0
    position = None
    
    for index, row in df.iterrows():
        if row['rsi'] < 30 and row['macd'] > row['macd_signal']:
            # Buy signal
            position_size = calculate_position_size(risk_per_trade, row['close'], 0.01)
            position = (row['close'], position_size)
            trades.append({
                'type': 'buy',
                'timestamp': row['timestamp'],
                'price': row['close'],
                'size': position_size
            })
        elif row['rsi'] > 70 and row['macd'] < row['macd_signal']:
            # Sell signal
            if position:
                trades.append({
                    'type': 'sell',
                    'timestamp': row['timestamp'],
                    'price': row['close'],
                    'size': position[1]
                })
                position = None
    
    # Calculate performance
    total_profit = sum((trade['price'] - position[0]) * trade['size'] for trade in trades if trade['type'] == 'sell')
    num_trades = len(trades)
    
    # Export results
    results = {
        'strategy': 'Test Strategy',
        'symbol': symbol,
        'timeframe': '1Min',
        'start_date': start_date,
        'end_date': end_date,
        'total_profit': total_profit,
        'num_trades': num_trades,
        'trades': trades
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()