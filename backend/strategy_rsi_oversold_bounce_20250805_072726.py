"""
Generated Strategy: RSI Oversold Bounce
Description: Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.
Generated: 2025-08-05 07:27:26
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

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
        response = requests.get(f'{BASE_URL}/v2/data', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['data'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(portfolio_value, risk_percent, stop_loss_pct):
    try:
        position_size = (portfolio_value * risk_percent) / stop_loss_pct
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    risk_per_trade = 0.01
    portfolio_value = 100000  # Initial portfolio value
    
    data = get_data(symbol, start_date, end_date)
    if data is None:
        return
    
    data['close'] = pd.to_numeric(data['close'])
    data['RSI'] = ta.momentum.RSIIndicator(data['close'], window=14).rsi()
    
    trades = []
    position_size = 0
    in_position = False
    
    for index, row in data.iterrows():
        if not in_position and row['RSI'] < 30:
            # Calculate position size based on risk
            position_size = calculate_position_size(portfolio_value, risk_per_trade, 0.02)  # Assuming 2% stop loss
            if position_size > 0:
                entry_price = row['close']
                entry_time = row['timestamp']
                in_position = True
                trades.append({
                    'entry_time': entry_time,
                    'entry_price': entry_price,
                    'position_size': position_size
                })
        
        elif in_position and (row['RSI'] >= 50 or (row['close'] - entry_price) / entry_price >= 0.02):
            exit_price = row['close']
            exit_time = row['timestamp']
            pnl = (exit_price - entry_price) / entry_price * position_size
            portfolio_value += pnl
            in_position = False
            trades[-1]['exit_time'] = exit_time
            trades[-1]['exit_price'] = exit_price
            trades[-1]['pnl'] = pnl
    
    results = {
        'trades': trades,
        'total_profit': sum(t['pnl'] for t in trades if 'pnl' in t),
        'number_of_trades': len(trades),
        'win_rate': sum(1 for t in trades if 'pnl' in t and t['pnl'] > 0) / len(trades) if trades else 0
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()