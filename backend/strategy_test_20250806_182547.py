"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:25:47
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
            'limit': 1000
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        return pd.json_normalize(response.json()['bars'])
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_position_size(account_balance, risk_percent, stop_loss):
    try:
        position_size = (account_balance * risk_percent) / stop_loss
        return position_size
    except:
        return 0

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    risk_percent = 0.01
    
    data = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if data is None:
        return
    
    data['time'] = pd.to_datetime(data['time'])
    data.set_index('time', inplace=True)
    
    data['SMA_20'] = data['close'].rolling(20).mean()
    data['SMA_50'] = data['close'].rolling(50).mean()
    
    trades = []
    position = None
    account_balance = 100000
    stop_loss_pct = 0.02
    
    for i in range(len(data)):
        row = data.iloc[i]
        
        if i < 50:
            continue
            
        if row['SMA_20'] > row['SMA_50'] and position != 'long':
            # Buy signal
            position = 'long'
            entry_price = row['close']
            stop_loss = entry_price * (1 - stop_loss_pct)
            position_size = calculate_position_size(account_balance, risk_percent, entry_price - stop_loss)
            
            trades.append({
                'type': 'buy',
                'entry': entry_price,
                'exit': None,
                'size': position_size,
                'stop_loss': stop_loss
            })
            
        elif row['SMA_20'] < row['SMA_50'] and position == 'long':
            # Sell signal
            position = None
            exit_price = row['close']
            last_trade = trades[-1]
            last_trade['exit'] = exit_price
            last_trade['profit'] = (exit_price - last_trade['entry']) * last_trade['size']
            
    performance = {
        'total_profit': sum(t['profit'] for t in trades if 'profit' in t),
        'number_of_trades': len(trades),
        'win_rate': sum(1 for t in trades if t.get('profit', 0) > 0) / len(trades) if trades else 0
    }
    
    results = {
        'trades': trades,
        'performance': performance
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()