"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 17:48:28
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

def fetch_data(symbol, start_date, end_date):
    try:
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': '1Min',
            'limit': 10000
        }
        response = requests.get(f'{ALPACA_BASE_URL}/v2/data', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['data'])
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_macd(df):
    df['MACD'], df['MACD_Signal'], df['MACD_Histogram'] = ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).macd(), ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).macd_signal(), ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).macd_diff()
    return df

def backtest_macd_crossover(df, initial_capital=100000):
    df = df.sort_values('timestamp')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    trades = []
    position_size = 0
    macd = df['MACD']
    signal = df['MACD_Signal']
    
    for i in range(1, len(df)):
        current_row = df.iloc[i]
        prev_row = df.iloc[i-1]
        
        if macd.iloc[i] > signal.iloc[i] and macd.iloc[i-1] < signal.iloc[i-1]:
            if position_size == 0:
                risk_amount = initial_capital * 0.01
                position_size = risk_amount / (current_row['close'] * 0.02)
                trades.append({
                    'type': 'buy',
                    'timestamp': current_row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                    'price': current_row['close'],
                    'position_size': position_size
                })
        
        elif macd.iloc[i] < signal.iloc[i] and macd.iloc[i-1] > signal.iloc[i-1]:
            if position_size > 0:
                trades.append({
                    'type': 'sell',
                    'timestamp': current_row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                    'price': current_row['close'],
                    'position_size': position_size
                })
                position_size = 0
    
    return trades

def calculate_performance(trades, initial_capital):
    total_profit = 0
    winners = 0
    total_trades = len(trades)
    
    for i in range(0, len(trades), 2):
        if i+1 >= len(trades):
            break
        buy_price = trades[i]['price']
        sell_price = trades[i+1]['price']
        profit = (sell_price - buy_price) * trades[i]['position_size']
        total_profit += profit
        if profit > 0:
            winners += 1
    
    return {
        'total_profit': total_profit,
        'total_trades': total_trades,
        'winning_trades': winners,
        'profit_percentage': (total_profit / initial_capital) * 100
    }

def main():
    try:
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        symbol = 'QQQ'
        
        df = fetch_data(symbol, start_date, end_date)
        if df is None:
            return
            
        df = df[['timestamp', 'open', 'high', 'low', 'close']]
        df = calculate_macd(df)
        
        trades = backtest_macd_crossover(df)
        performance = calculate_performance(trades, initial_capital=100000)
        
        results = {
            'trades': trades,
            'performance': performance
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully!')
        
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()