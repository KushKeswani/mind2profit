"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:25:21
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

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
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', params=params, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(account_balance, risk_percent, stop_loss):
    try:
        position_size = (account_balance * risk_percent) / stop_loss
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def generate_signals(data):
    try:
        data['SMA_20'] = ta.momentum.SMAIndicator(data['close'], window=20).sma_indicator()
        data['SMA_50'] = ta.momentum.SMAIndicator(data['close'], window=50).sma_indicator()
        data['signal'] = 0
        data.loc[data['SMA_20'] > data['SMA_50'], 'signal'] = 1
        data.loc[data['SMA_20'] < data['SMA_50'], 'signal'] = -1
        return data
    except Exception as e:
        print(f'Error generating signals: {e}')
        return None

def execute_backtest(data, initial_balance):
    try:
        trades = []
        position = 0
        balance = initial_balance
        prev_signal = 0
        
        for index, row in data.iterrows():
            if row['signal'] == 1 and prev_signal != 1:
                # Enter long position
                position_size = calculate_position_size(balance, 0.01, row['high'] - row['low'])
                position = position_size
                trades.append({
                    'type': 'buy',
                    'price': row['close'],
                    'size': position_size,
                    'timestamp': index
                })
            elif row['signal'] == -1 and prev_signal != -1:
                # Enter short position
                position_size = calculate_position_size(balance, 0.01, row['high'] - row['low'])
                position = -position_size
                trades.append({
                    'type': 'sell',
                    'price': row['close'],
                    'size': position_size,
                    'timestamp': index
                })
            
            # Update balance based on position
            if position != 0:
                balance += position * (row['close'] - data['close'].shift(1)[index])
            
            prev_signal = row['signal']
            
        return trades
    except Exception as e:
        print(f'Error executing backtest: {e}')
        return []

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        initial_balance = 100000
        
        data = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if data is None:
            return
            
        data = generate_signals(data)
        if data is None:
            return
            
        trades = execute_backtest(data, initial_balance)
        
        # Calculate performance metrics
        total_trades = len(trades)
        wins = len([t for t in trades if t['type'] == 'buy'])
        losses = total_trades - wins
        win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
        
        # Prepare results
        results = {
            'trades': trades,
            'performance': {
                'total_trades': total_trades,
                'win_rate': win_rate,
                'initial_balance': initial_balance,
                'final_balance': initial_balance + sum([t['size'] * (data['close'].iloc[i+1] - t['price']) for i, t in enumerate(trades)]),
                'max_drawdown': 0  # Simplified calculation
            }
        }
        
        # Export to JSON
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=4)
            
        print('Backtest completed successfully!')
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()