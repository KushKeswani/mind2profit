"""
Generated Strategy: RSI Oversold Bounce
Description: Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.
Generated: 2025-08-05 07:22:12
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
    try:
        endpoint = f'{BASE_URL}/v2/data/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
        headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
        response = requests.get(endpoint, headers=headers)
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_rsi(data, period=14):
    return data['close'].ta.rsi(length=period)

def run_strategy(data):
    data['rsi'] = calculate_rsi(data)
    trades = []
    position_size = 0
    equity = 100000
    risk_per_trade = 0.01
    
    for i in range(len(data)):
        if data.iloc[i]['rsi'] < 30 and position_size == 0:
            # Calculate position size based on risk management
            price = data.iloc[i]['close']
            position_size = (equity * risk_per_trade) / price
            entry_price = price
            entry_time = data.iloc[i]['timestamp']
            trades.append({'type': 'buy', 'price': entry_price, 'time': entry_time})
            
        elif data.iloc[i]['rsi'] > 50 and position_size > 0:
            exit_price = data.iloc[i]['close']
            exit_time = data.iloc[i]['timestamp']
            pnl = (exit_price - entry_price) * position_size
            equity += pnl
            trades.append({'type': 'sell', 'price': exit_price, 'time': exit_time})
            position_size = 0
            
    return trades

def export_to_json(trades, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(trades, f, indent=2)
        return True
    except Exception as e:
        print(f'Error exporting to JSON: {e}')
        return False

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    
    data = get_data(symbol, start_date, end_date)
    if data is None:
        return
        
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)
    
    trades = run_strategy(data)
    if not trades:
        print('No trades executed')
        return
        
    export_to_json(trades, 'strategy_results.json')
    print('Strategy results exported to strategy_results.json')

if __name__ == "__main__":
    main()