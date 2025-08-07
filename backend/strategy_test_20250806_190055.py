"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 19:00:55
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, start_date, end_date):
    try:
        endpoint = f'{BASE_URL}/v2/data/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
        headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return pd.DataFrame(response.json()['bars'])
        return None
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['SMA_20'] = ta.momentum.SMAIndicator(df['close'], window=20).sma_indicator()
        df['SMA_50'] = ta.momentum.SMAIndicator(df['close'], window=50).sma_indicator()
        df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def get_position_size(account_balance, risk_percent, stop_loss):
    try:
        position_size = (account_balance * risk_percent) / stop_loss
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def generate_signals(df):
    try:
        signals = []
        active_trade = None
        for i in range(len(df)):
            if df['SMA_20'].iloc[i] > df['SMA_50'].iloc[i] and df['SMA_20'].iloc[i-1] < df['SMA_50'].iloc[i-1]:
                signals.append({'type': 'buy', 'price': df['close'].iloc[i], 'time': df['timestamp'].iloc[i]})
                active_trade = 'long'
            elif df['SMA_20'].iloc[i] < df['SMA_50'].iloc[i] and df['SMA_20'].iloc[i-1] > df['SMA_50'].iloc[i-1]:
                if active_trade:
                    signals.append({'type': 'sell', 'price': df['close'].iloc[i], 'time': df['timestamp'].iloc[i]})
                    active_trade = None
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return []

def backtest(df, signals):
    try:
        trades = []
        account_balance = 100000
        risk_percent = 0.01
        for signal in signals:
            if signal['type'] == 'buy':
                stop_loss = signal['price'] - 2 * df['ATR'].iloc[df.index.get_loc(signal['time')]
                position_size = get_position_size(account_balance, risk_percent, signal['price'] - stop_loss)
                if position_size > 0:
                    trades.append({
                        'type': 'enter',
                        'entry_price': signal['price'],
                        'entry_time': signal['time'],
                        'position_size': position_size,
                        'stop_loss': stop_loss
                    })
            elif signal['type'] == 'sell':
                if len(trades) > 0 and trades[-1]['type'] == 'enter':
                    profit = signal['price'] - trades[-1]['entry_price']
                    trades.append({
                        'type': 'exit',
                        'exit_price': signal['price'],
                        'exit_time': signal['time'],
                        'profit': profit
                    })
        return trades
    except Exception as e:
        print(f'Error backtesting: {e}')
        return []

def export_results(trades, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(trades, f, indent=2)
        return True
    except Exception as e:
        print(f'Error exporting results: {e}')
        return False

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        df = get_data(symbol, start_date, end_date)
        if df is not None:
            df = calculate_indicators(df)
            if df is not None:
                signals = generate_signals(df)
                if signals:
                    trades = backtest(df, signals)
                    if trades:
                        export_results(trades, 'backtest_results.json')
                        print('Backtest completed successfully')
                    else:
                        print('No trades generated')
                else:
                    print('No signals generated')
            else:
                print('Error calculating indicators')
        else:
            print('Error fetching data')
    except Exception as e:
        print(f'Error in main: {e}')

if __name__ == "__main__":
    main()