"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-07 11:19:15
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
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_macd(df):
    df['MACD'], df['SIGNAL'] = ta.momentum.MACD(df['close']).macd(), ta.momentum.MACD(df['close']).signal()
    return df

def generate_signals(df):
    df['SIGNAL'] = 0
    df.loc[df['MACD'] > df['SIGNAL'], 'SIGNAL'] = 1
    df.loc[df['MACD'] < df['SIGNAL'], 'SIGNAL'] = -1
    return df

def calculate_position_size(account_balance, risk_percent, stop_loss_pct):
    position_size = (account_balance * risk_percent) / stop_loss_pct
    return position_size

def execute_trade(symbol, qty, side):
    try:
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        data = {
            'symbol': symbol,
            'qty': str(qty),
            'side': side,
            'type': 'market',
            'time_in_force': 'gtc'
        }
        response = requests.post(f'{BASE_URL}/v2/orders', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f'Error executing trade: {e}')
        return None

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    risk_percent = 0.01
    stop_loss_pct = 0.01  # 1% stop loss
    
    df = get_data(symbol, start_date, end_date)
    if df is None:
        return
    
    df = calculate_macd(df)
    df = generate_signals(df)
    
    account_balance = 100000  # Initial balance
    position_size = calculate_position_size(account_balance, risk_percent, stop_loss_pct)
    
    trades = []
    qty = 0
    current_price = 0
    
    for index, row in df.iterrows():
        if row['SIGNAL'] == 1 and qty == 0:
            # Buy signal
            current_price = row['close']
            qty = int(position_size / current_price)
            if qty > 0:
                trade = execute_trade(symbol, qty, 'buy')
                if trade:
                    trades.append({
                        'type': 'buy',
                        'price': current_price,
                        'qty': qty,
                        'timestamp': index
                    })
        elif row['SIGNAL'] == -1 and qty > 0:
            # Sell signal
            current_price = row['close']
            if execute_trade(symbol, qty, 'sell'):
                trades.append({
                    'type': 'sell',
                    'price': current_price,
                    'qty': qty,
                    'timestamp': index
                })
                qty = 0
    
    results = {
        'trades': trades,
        'performance': {
            'total_trades': len(trades),
            'final_balance': account_balance * (1 + (sum(1 for trade in trades if trade['type'] == 'sell') / len(trades)) * 0.01),
            'win_rate': sum(1 for trade in trades if trade['type'] == 'sell') / len(trades) if trades else 0
        }
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()