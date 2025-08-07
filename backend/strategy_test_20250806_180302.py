"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:03:02
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
    try:
        headers = {'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}
        params = {'symbol': symbol, 'start': start_date, 'end': end_date, 'timeframe': '1Min'}
        response = requests.get(f'{BASE_URL}/v2/data', params=params, headers=headers)
        return pd.DataFrame(response.json()['data'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['SMA_20'] = ta.moving_average(df['close'], window=20)
        df['SMA_50'] = ta.moving_average(df['close'], window=50)
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def generate_signals(df):
    try:
        signals = []
        for i in range(len(df)):
            if df['SMA_20'].iloc[i] > df['SMA_50'].iloc[i] and df['SMA_20'].iloc[i-1] < df['SMA_50'].iloc[i-1]:
                signals.append({'type': 'buy', 'price': df['close'].iloc[i], 'time': df.index[i]})
            elif df['SMA_20'].iloc[i] < df['SMA_50'].iloc[i] and df['SMA_20'].iloc[i-1] > df['SMA_50'].iloc[i-1]:
                signals.append({'type': 'sell', 'price': df['close'].iloc[i], 'time': df.index[i]})
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return None

def calculate_position_size(risk_percent, current_price, buying_power):
    try:
        position_size = (buying_power * risk_percent) / 100 / current_price
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def get_buying_power():
    try:
        headers = {'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}
        response = requests.get(f'{BASE_URL}/v2/account', headers=headers)
        return float(response.json()['cash'])
    except Exception as e:
        print(f'Error getting buying power: {e}')
        return 0

def calculate_performance(trades):
    try:
        total_pnl = sum(t['pnl'] for t in trades)
        total_return = (total_pnl / sum(t['entry'] * t['size'] for t in trades)) * 100
        sharpe_ratio = (total_return / (pd.Series([t['pnl'] for t in trades]).std())) * (252**0.5)
        return {'total_return': total_return, 'sharpe_ratio': sharpe_ratio}
    except Exception as e:
        print(f'Error calculating performance: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_percent = 1.0
        
        df = get_data(symbol, start_date, end_date)
        if df is None:
            return
            
        df = calculate_indicators(df)
        if df is None:
            return
            
        signals = generate_signals(df)
        if signals is None:
            return
            
        buying_power = get_buying_power()
        if buying_power == 0:
            return
            
        trades = []
        position_size = 0
        for signal in signals:
            if signal['type'] == 'buy':
                position_size = calculate_position_size(risk_percent, signal['price'], buying_power)
                if position_size == 0:
                    continue
                trades.append({
                    'type': 'buy',
                    'entry': signal['price'],
                    'size': position_size,
                    'time': signal['time']
                })
            elif signal['type'] == 'sell':
                if len(trades) == 0 or trades[-1]['type'] != 'buy':
                    continue
                last_trade = trades[-1]
                pnl = signal['price'] - last_trade['entry']
                last_trade['exit'] = signal['price']
                last_trade['pnl'] = pnl * last_trade['size']
        
        performance = calculate_performance(trades)
        if performance is None:
            return
            
        results = {
            'trades': trades,
            'performance': performance,
            'symbol': symbol,
            'timeframe': '1Min',
            'start_date': start_date,
            'end_date': end_date
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully')
        
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()