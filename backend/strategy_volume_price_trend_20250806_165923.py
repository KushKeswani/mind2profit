"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 16:59:23
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
BASE_URL = 'https://paper-api.alpaca.markets'

def get_data(symbol, timeframe, start_date, end_date):
    try:
        data = requests.get(
            f'{BASE_URL}/v2/data/{symbol}/bars/{timeframe}',
            params={
                'start': start_date,
                'end': end_date,
                'limit': 1000
            },
            headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
        )
        return pd.DataFrame(data.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['mfi'] = ta.momentum.MFIIndicator(df['high'], df['low'], df['close'], df['volume'], window=14).mfi()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def generate_signals(df):
    try:
        signals = []
        in_trade = False
        for i in range(len(df)):
            if not in_trade and df['mfi'].iloc[i] > 20 and df['close'].iloc[i] > df['sma_20'].iloc[i]:
                signals.append({'type': 'buy', 'price': df['close'].iloc[i], 'time': df.index[i]})
                in_trade = True
            elif in_trade and (df['mfi'].iloc[i] < 80 or df['close'].iloc[i] < df['sma_20'].iloc[i]):
                signals.append({'type': 'sell', 'price': df['close'].iloc[i], 'time': df.index[i]})
                in_trade = False
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return []

def calculate_position_size(df, risk_percent):
    try:
        initial_capital = 100000
        position_size = []
        for i in range(len(df)):
            atr = df['atr'].iloc[i]
            stop_loss = atr * 2
            position_size.append((initial_capital * risk_percent / 100) / stop_loss)
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return []

def execute_trades(signals, position_size):
    try:
        trades = []
        for i in range(len(signals)):
            if signals[i]['type'] == 'buy':
                entry_price = signals[i]['price']
                size = position_size[i]
                next_signal = next((s for s in signals[i+1:] if s['type'] == 'sell'), None)
                if next_signal:
                    exit_price = next_signal['price']
                    pnl = (exit_price - entry_price) * size
                    trades.append({
                        'entry_time': signals[i]['time'].strftime('%Y-%m-%dT%H:%M:%S'),
                        'exit_time': next_signal['time'].strftime('%Y-%m-%dT%H:%M:%S'),
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'position_size': size,
                        'pnl': pnl
                    })
        return trades
    except Exception as e:
        print(f'Error executing trades: {e}')
        return []

def main():
    try:
        symbol = 'QQQ'
        timeframe = '1Min'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_percent = 1.0
        
        df = get_data(symbol, timeframe, start_date, end_date)
        if df is None:
            return
            
        df = calculate_indicators(df)
        if df is None:
            return
            
        signals = generate_signals(df)
        if not signals:
            return
            
        position_size = calculate_position_size(df, risk_percent)
        if not position_size:
            return
            
        trades = execute_trades(signals, position_size)
        if not trades:
            return
            
        total_profit = sum(t['pnl'] for t in trades)
        num_trades = len(trades)
        win_rate = sum(1 for t in trades if t['pnl'] > 0) / num_trades if num_trades > 0 else 0
        
        results = {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'win_rate': win_rate,
            'trades': trades
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully')
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()