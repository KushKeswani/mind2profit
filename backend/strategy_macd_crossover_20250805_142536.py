"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-05 14:25:36
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
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
        data = response.json()
        df = pd.DataFrame(data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_macd(df):
    try:
        macd_indicator = ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd_indicator.macd()
        df['signal'] = macd_indicator.signal()
        return df
    except Exception as e:
        print(f'Error calculating MACD: {e}')
        return None

def backtest_strategy(df):
    try:
        trades = []
        position = 'flat'
        balance = 100000
        risk_per_trade = 0.01
        
        for i in range(1, len(df)):
            current_row = df.iloc[i]
            prev_row = df.iloc[i-1]
            
            if current_row['macd'] > current_row['signal'] and prev_row['macd'] < prev_row['signal']:
                if position == 'flat':
                    entry_price = current_row['open']
                    position_size = calculate_position_size(balance, entry_price, risk_per_trade)
                    trades.append({
                        'type': 'buy',
                        'entry_time': current_row.name.isoformat(),
                        'entry_price': entry_price,
                        'shares': position_size
                    })
                    position = 'long'
            elif current_row['macd'] < current_row['signal'] and prev_row['macd'] > prev_row['signal']:
                if position == 'long':
                    exit_price = current_row['open']
                    profit = (exit_price - entry_price) * position_size
                    balance += profit
                    trades.append({
                        'type': 'sell',
                        'exit_time': current_row.name.isoformat(),
                        'exit_price': exit_price,
                        'profit': profit
                    })
                    position = 'flat'
        
        return {
            'trades': trades,
            'total_trades': len(trades),
            'profit': sum(t['profit'] for t in trades if t['type'] == 'sell'),
            'win_rate': len([t for t in trades if t['type'] == 'sell' and t['profit'] > 0]) / len(trades) * 100
        }
    except Exception as e:
        print(f'Error running backtest: {e}')
        return None

def calculate_position_size(balance, entry_price, risk_percent):
    try:
        risk_amount = balance * risk_percent
        position_size = risk_amount / (2 * entry_price)
        return int(position_size)
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        df = get_data(symbol, start_date, end_date)
        if df is not None:
            df = calculate_macd(df)
            if df is not None:
                results = backtest_strategy(df)
                if results is not None:
                    with open('backtest_results.json', 'w') as f:
                        json.dump(results, f, indent=2)
                    print('Backtest completed successfully')
                else:
                    print('Backtest failed')
            else:
                print('MACD calculation failed')
        else:
            print('Data fetching failed')
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == "__main__":
    main()