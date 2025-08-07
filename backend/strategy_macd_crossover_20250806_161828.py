"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 16:18:28
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        
        headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe,
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_macd(df):
    df['macd'] = ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).macd()
    df['signal'] = ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).signal()
    return df

def generate_signals(df):
    signals = []
    in_position = False
    for i in range(1, len(df)):
        prev_macd = df['macd'].iloc[i-1]
        prev_signal = df['signal'].iloc[i-1]
        curr_macd = df['macd'].iloc[i]
        curr_signal = df['signal'].iloc[i]
        
        if not in_position and curr_macd > curr_signal and prev_macd < prev_signal:
            signals.append({'type': 'buy', 'time': df.index[i], 'price': df['close'].iloc[i]})
            in_position = True
        elif in_position and curr_macd < curr_signal and prev_macd > prev_signal:
            signals.append({'type': 'sell', 'time': df.index[i], 'price': df['close'].iloc[i]})
            in_position = False
    return signals

def calculate_position_size(portfolio_value, risk_percent, stop_loss_pct):
    return (portfolio_value * risk_percent) / stop_loss_pct

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    risk_percent = 0.01
    portfolio_value = 100000
    
    df = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if df is None:
        print("Failed to retrieve data")
        return
    
    df = df.drop(columns=['exchange'])
    df.index = pd.to_datetime(df['timestamp'])
    df = df.drop(columns=['timestamp'])
    
    df = calculate_macd(df)
    signals = generate_signals(df)
    
    trades = []
    position_size = calculate_position_size(portfolio_value, risk_percent, 0.02)
    
    for signal in signals:
        if signal['type'] == 'buy':
            trades.append({
                'type': 'buy',
                'entry_time': str(signal['time']),
                'entry_price': signal['price'],
                'quantity': int(position_size / signal['price'])
            })
        else:
            trades.append({
                'type': 'sell',
                'exit_time': str(signal['time']),
                'exit_price': signal['price'],
                'quantity': int(position_size / signal['price'])
            })
    
    results = {
        'trades': trades,
        'total_trades': len(trades),
        'start_date': start_date,
        'end_date': end_date,
        'symbol': symbol
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Backtest completed. Results saved to backtest_results.json")

if __name__ == "__main__":
    main()