"""
Generated Strategy: Moving Average Crossover
Description: Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.
Generated: 2025-08-01 20:44:03
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta
import os

# API Configuration
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', 'PK0F1YSWGZYNHF1VKOY5')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY', 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB')
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

def get_historical_data(symbol, start_date, end_date):
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
        
        data = pd.DataFrame(response.json()['data'])
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data.set_index('timestamp', inplace=True)
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(data):
    try:
        data['sma_20'] = ta.moving_average(data['close'], window=20)
        data['sma_50'] = ta.moving_average(data['close'], window=50)
        return data
    
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def moving_average_crossover_strategy(data):
    try:
        trades = []
        position = None
        
        for i in range(len(data)):
            if data.index[i] < pd.to_datetime('2025-01-01'):
                continue
            if data.index[i] > pd.to_datetime('2025-03-01'):
                break
            
            current_row = data.iloc[i]
            
            if current_row['sma_20'] > current_row['sma_50'] and position != 'long':
                if i > 0 and data.iloc[i-1]['sma_20'] <= data.iloc[i-1]['sma_50']:
                    entry_price = current_row['close']
                    entry_time = current_row.name
                    position = 'long'
                    trades.append({'type': 'buy', 'entry_time': entry_time, 'entry_price': entry_price})
            
            elif current_row['sma_20'] < current_row['sma_50'] and position == 'long':
                if i > 0 and data.iloc[i-1]['sma_20'] >= data.iloc[i-1]['sma_50']:
                    exit_price = current_row['close']
                    exit_time = current_row.name
                    position = None
                    profit = exit_price - trades[-1]['entry_price']
                    duration = (exit_time - trades[-1]['entry_time']).total_seconds() / 60
                    trades[-1]['exit_time'] = exit_time
                    trades[-1]['exit_price'] = exit_price
                    trades[-1]['profit'] = profit
                    trades[-1]['duration'] = duration
        
        return trades
    
    except Exception as e:
        print(f"Error executing strategy: {e}")
        return None

def analyze_results(trades):
    try:
        if not trades:
            return None
            
        total_profit = sum(t['profit'] for t in trades)
        num_trades = len(trades)
        avg_profit = total_profit / num_trades if num_trades > 0 else 0
        win_rate = sum(1 for t in trades if t['profit'] > 0) / num_trades * 100 if num_trades > 0 else 0
        
        results = {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'avg_profit': avg_profit,
            'win_rate': win_rate,
            'trades': trades
        }
        
        return results
    
    except Exception as e:
        print(f"Error analyzing results: {e}")
        return None

def main():
    try:
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        symbol = 'QQQ'
        
        data = get_historical_data(symbol, start_date, end_date)
        if data is None:
            print("Failed to fetch data")
            return
        
        data = calculate_indicators(data)
        if data is None:
            print("Failed to calculate indicators")
            return
        
        trades = moving_average_crossover_strategy(data)
        if trades is None:
            print("Failed to execute strategy")
            return
        
        results = analyze_results(trades)
        if results is None:
            print("Failed to analyze results")
            return
        
        results_json = json.dumps(results, default=str, indent=2)
        print(results_json)
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, default=str, indent=2)
            
    except Exception as e:
        print(f"Main execution error: {e}")

if __name__ == '__main__':
    main()