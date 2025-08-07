"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 15:04:40
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
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/ags/slice', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['data'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_macd(df):
    macd = ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd'] = macd.macd()
    df['signal'] = macd.signal()
    df['rsi'] = ta.momentum.RSI(df['close'], window=14)
    return df

def generate_signals(df):
    signals = []
    in_position = False
    for i in range(1, len(df)):
        prev_macd = df['macd'].iloc[i-1]
        curr_macd = df['macd'].iloc[i]
        prev_signal = df['signal'].iloc[i-1]
        curr_signal = df['signal'].iloc[i]
        
        if not in_position and curr_macd > curr_signal and prev_macd < prev_signal:
            signals.append({'type': 'buy', 'time': df.index[i], 'price': df['close'].iloc[i]})
            in_position = True
        elif in_position and curr_macd < curr_signal and prev_macd > prev_signal:
            signals.append({'type': 'sell', 'time': df.index[i], 'price': df['close'].iloc[i]})
            in_position = False
    return signals

def calculate_position_size(entry_price, risk_amount, stop_loss_pct):
    position_size = (risk_amount * 0.01) / (stop_loss_pct * entry_price)
    return position_size

def backtest_strategy():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    risk_per_trade = 1000  # $1000 risk per trade (1% of $100,000 account)
    
    df = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if df is None:
        return
    
    df = df.rename(columns={'timestamp': 'time'})
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    
    df = calculate_macd(df)
    signals = generate_signals(df)
    
    trades = []
    for signal in signals:
        if signal['type'] == 'buy':
            entry_price = signal['price']
            stop_loss_price = entry_price * (1 - 0.02)  # 2% stop loss
            position_size = calculate_position_size(entry_price, risk_per_trade, 0.02)
            
            sell_signal = next((s for s in signals if s['type'] == 'sell' and s['time'] > signal['time']), None)
            if sell_signal:
                exit_price = sell_signal['price']
                pnl = (exit_price - entry_price) * position_size
                trades.append({
                    'entry_time': signal['time'].isoformat(),
                    'exit_time': sell_signal['time'].isoformat(),
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'position_size': position_size,
                    'pnl': pnl
                })
    
    total_pnl = sum(t['pnl'] for t in trades)
    num_trades = len(trades)
    win_rate = sum(1 for t in trades if t['pnl'] > 0) / num_trades if num_trades > 0 else 0
    
    results = {
        'total_pnl': total_pnl,
        'num_trades': num_trades,
        'win_rate': win_rate,
        'trades': trades
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)

def main():
    try:
        backtest_strategy()
        print("Backtest completed successfully. Results exported to backtest_results.json")
    except Exception as e:
        print(f"Error in backtest: {e}")

if __name__ == "__main__":
    main()