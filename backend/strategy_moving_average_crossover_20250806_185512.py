"""
Generated Strategy: Moving Average Crossover
Description: Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.
Generated: 2025-08-06 18:55:12
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Alpaca API Configuration
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
    try:
        header = {'APCA-API-KEY-ID': ALPACA_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}
        params = {'symbol': symbol, 'start': start_date, 'end': end_date, 'timeframe': '1Min'}
        response = requests.get(f'{ALPACA_BASE_URL}/v2/data', headers=header, params=params)
        data = response.json()
        df = pd.DataFrame(data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['sma_20'] = ta.momentum.SMAIndicator(df['close']).sma_indicator()
        df['sma_50'] = ta.momentum.SMAIndicator(df['close'], window=50).sma_indicator()
        df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def backtest_strategy(df, initial_capital=100000):
    try:
        trades = []
        position = 0
        cash = initial_capital
        equity = initial_capital
        previous_signal = 0
        
        for index, row in df.iterrows():
            if row['sma_20'] > row['sma_50'] and previous_signal != 1:
                # Buy signal
                position_size = (0.01 * equity) / (row['close'] - (row['close'] - row['atr']))
                position_size = position_size.round(2)
                if position_size > 0:
                    position = position_size
                    cash -= position * row['close']
                    equity = cash + position * row['close']
                    trades.append({
                        'timestamp': index.strftime('%Y-%m-%dT%H:%M:%S'),
                        'type': 'buy',
                        'price': row['close'],
                        'quantity': position_size
                    })
                previous_signal = 1
            elif row['sma_20'] < row['sma_50'] and previous_signal != -1:
                # Sell signal
                if position > 0:
                    cash += position * row['close']
                    equity = cash + position * row['close']
                    position = 0
                    trades.append({
                        'timestamp': index.strftime('%Y-%m-%dT%H:%M:%S'),
                        'type': 'sell',
                        'price': row['close'],
                        'quantity': position_size
                    })
                previous_signal = -1
        return trades
    except Exception as e:
        print(f'Error executing strategy: {e}')
        return None

def calculate_performance(trades, initial_capital):
    try:
        if not trades:
            return None
        total_return = (initial_capital + sum(t['price'] * t['quantity'] if t['type'] == 'sell' else -t['price'] * t['quantity'] for t in trades)) / initial_capital
        num_trades = len(trades)
        wins = sum(1 for t in trades if t['type'] == 'sell' and t['price'] > trades[trades.index(t)-1]['price'])
        losses = num_trades // 2 - wins
        sharpe_ratio = (total_return / (len(trades)/2)) ** 0.5
        return {
            'total_return': total_return,
            'num_trades': num_trades,
            'win_rate': wins / (wins + losses),
            'sharpe_ratio': sharpe_ratio
        }
    except Exception as e:
        print(f'Error calculating performance: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        df = get_data(symbol, start_date, end_date)
        if df is None:
            return
            
        df = calculate_indicators(df)
        if df is None:
            return
            
        trades = backtest_strategy(df)
        if trades is None:
            return
            
        performance = calculate_performance(trades, 100000)
        if performance is None:
            return
            
        results = {
            'trades': trades,
            'performance': performance
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully')
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == "__main__":
    main()