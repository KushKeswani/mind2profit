"""
Generated Strategy: RSI Oversold Bounce
Description: Buy when RSI goes below 30 (oversold), sell when it reaches 50 or profit target. Use 14-period RSI with 30/50 levels.
Generated: 2025-08-05 07:20:52
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
        endpoint = f'{BASE_URL}/v2/data/{symbol}/minute'
        params = {
            'start': start_date,
            'end': end_date,
            'limit': 1000
        }
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        response = requests.get(endpoint, params=params, headers=headers)
        if response.status_code == 200:
            return pd.DataFrame(response.json()['bars'])
        return None
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_rsi(data, period=14):
    return data['close'].ta.rsi(length=period)

def calculate_position_size(entry_price, risk_amount, stop_loss_pct):
    stop_loss = entry_price * (1 - stop_loss_pct)
    position_size = risk_amount / (entry_price - stop_loss)
    return position_size

def backtest_strategy(data):
    trades = []
    position = None
    risk_per_trade = 0.01  # 1% risk per trade
    initial_capital = 100000
    capital = initial_capital
    stop_loss_pct = 0.02  # 2% stop loss
    take_profit_pct = 0.02  # 2% profit target
    
    data['rsi'] = calculate_rsi(data)
    
    for index, row in data.iterrows():
        if not position:
            if row['rsi'] < 30:
                position = {
                    'entry_time': row['time'],
                    'entry_price': row['close'],
                    'shares': calculate_position_size(row['close'], capital * risk_per_trade, stop_loss_pct)
                }
                trades.append({'type': 'buy', 'price': row['close'], 'time': row['time']})
        else:
            if row['rsi'] > 50 or row['close'] >= position['entry_price'] * (1 + take_profit_pct):
                position['exit_time'] = row['time']
                position['exit_price'] = row['close']
                position['pnl'] = position['exit_price'] - position['entry_price']
                position['shares'] = position['shares']
                
                capital += position['pnl'] * position['shares']
                trades.append({'type': 'sell', 'price': row['close'], 'time': row['time']})
                position = None
                
    return trades, capital

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        data = get_data(symbol, start_date, end_date)
        if data is None:
            print('Failed to retrieve data')
            return
            
        data['time'] = pd.to_datetime(data['time'])
        data.set_index('time', inplace=True)
        
        trades, final_capital = backtest_strategy(data)
        
        results = {
            'trades': trades,
            'initial_capital': 100000,
            'final_capital': final_capital,
            'profit': final_capital - 100000,
            'number_of_trades': len(trades),
            'win_rate': sum(1 for trade in trades if trade['type'] == 'sell' and trade['price'] > trades[trades.index(trade)-1]['price']) / (len(trades)/2)
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=4)
            
        print('Backtest completed successfully')
        
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()