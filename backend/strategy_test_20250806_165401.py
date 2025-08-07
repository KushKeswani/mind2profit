"""
Generated Strategy: Test
Description: Test strategy
Generated: 2025-08-06 16:54:01
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
    try:
        endpoint = f'{BASE_URL}/v2/data/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
        headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(risk_amount, stop_loss):
    try:
        position_size = risk_amount / stop_loss
        return round(position_size)
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def backtest_strategy(symbol, start_date, end_date, risk_percent):
    try:
        df = get_data(symbol, start_date, end_date)
        if df is None:
            return None
        
        df.reset_index(inplace=True)
        df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
        
        trades = []
        risk_amount = 100  # Fixed risk amount for calculation
        
        for i in range(len(df)):
            row = df.iloc[i]
            stop_loss = row['high'] + row['ATR']
            position_size = calculate_position_size(risk_amount, stop_loss - row['close'])
            
            if position_size > 0:
                trade = {
                    'entry_time': row['timestamp'],
                    'exit_time': df.iloc[i+1]['timestamp'] if i+1 < len(df) else row['timestamp'],
                    'position_size': position_size,
                    'entry_price': row['close'],
                    'stop_loss': stop_loss,
                    'risk': risk_amount,
                    'pnl': (df.iloc[i+1]['close'] - row['close']) * position_size if i+1 < len(df) else 0
                }
                trades.append(trade)
        
        total_pnl = sum(t['pnl'] for t in trades)
        num_trades = len(trades)
        win_rate = sum(1 for t in trades if t['pnl'] > 0) / num_trades if num_trades > 0 else 0
        
        results = {
            'total_pnl': total_pnl,
            'num_trades': num_trades,
            'win_rate': win_rate,
            'trades': trades
        }
        
        return results
    except Exception as e:
        print(f'Error in backtest strategy: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_percent = 0.01
        
        results = backtest_strategy(symbol, start_date, end_date, risk_percent)
        if results:
            print('Backtest Results:')
            print(json.dumps(results, indent=2))
            
            # Export to JSON
            with open('backtest_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            print('Results exported to backtest_results.json')
        else:
            print('Backtest failed')
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()