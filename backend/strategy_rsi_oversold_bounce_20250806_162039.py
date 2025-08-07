"""
Generated Strategy: RSI Oversold Bounce
Description: Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.
Generated: 2025-08-06 16:20:39
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date, timeframe):
    try:
        headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe
        }
        response = requests.get(f'{BASE_URL}/v2/data', params=params, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_rsi(data, period=14):
    return ta.momentum.RSI(data['close'], window=period)

def main():
    symbol = 'QQQ'
    timeframe = '1Min'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    risk_per_trade = 0.01
    rsi_period = 14
    rsi_lower = 30
    rsi_upper = 50
    profit_target = 0.02  # 2% profit target
    
    data = get_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    data['rsi'] = calculate_rsi(data, rsi_period)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    trades = []
    position_size = 0
    portfolio_value = 100000  # Initial portfolio value
    
    for i in range(len(data)):
        current_row = data.iloc[i]
        
        if current_row['rsi'] < rsi_lower and position_size == 0:
            # Calculate position size based on risk management
            position_size = (portfolio_value * risk_per_trade) / (current_row['close'] * 0.02)
            position_size = int(position_size)
            
            if position_size > 0:
                entry_price = current_row['close']
                entry_time = current_row['timestamp']
                trades.append({
                    'entry_time': str(entry_time),
                    'entry_price': entry_price,
                    'position_size': position_size
                })
        
        elif current_row['rsi'] > rsi_upper and position_size > 0:
            exit_price = current_row['close']
            exit_time = current_row['timestamp']
            profit = (exit_price - trades[-1]['entry_price']) * position_size
            portfolio_value += profit
            
            trades[-1]['exit_time'] = str(exit_time)
            trades[-1]['exit_price'] = exit_price
            trades[-1]['profit'] = profit
            position_size = 0
    
    results = {
        'trades': trades,
        'final_portfolio_value': portfolio_value
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()