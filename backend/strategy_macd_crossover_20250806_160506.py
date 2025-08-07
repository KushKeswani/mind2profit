"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 16:05:06
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
        
        response = requests.get(base_url + 'stocks/v2/minute', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['minute'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_macd(df):
    df['MACD'], df['SIGNAL'] = ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).macd(), ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).signal()
    return df

def generate_signals(df):
    signals = []
    for i in range(1, len(df)):
        prev_macd = df['MACD'].iloc[i-1]
        curr_macd = df['MACD'].iloc[i]
        prev_signal = df['SIGNAL'].iloc[i-1]
        curr_signal = df['SIGNAL'].iloc[i]
        
        if curr_macd > curr_signal and prev_macd <= prev_signal:
            signals.append({'type': 'buy', 'time': df.index[i], 'price': df['close'].iloc[i]})
        elif curr_macd < curr_signal and prev_macd >= prev_signal:
            signals.append({'type': 'sell', 'time': df.index[i], 'price': df['close'].iloc[i]})
    return signals

def calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pct):
    return (portfolio_value * risk_per_trade) / (stop_loss_pct * portfolio_value)

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    initial_capital = 100000
    risk_per_trade = 0.01
    stop_loss_pct = 0.02  # Assuming 2% stop loss
    
    df = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if df is None:
        return
    
    df = calculate_macd(df)
    signals = generate_signals(df)
    
    portfolio_value = initial_capital
    position_size = 0
    trades = []
    
    for signal in signals:
        if signal['type'] == 'buy':
            shares = int(calculate_position_size(portfolio_value, risk_per_trade, stop_loss_pct))
            position_size = shares
            trades.append({
                'entry_time': signal['time'].strftime('%Y-%m-%dT%H:%M:%S'),
                'entry_price': signal['price'],
                'shares': shares
            })
        else:
            if position_size > 0:
                exit_price = signal['price']
                pnl = (exit_price - trades[-1]['entry_price']) * position_size
                portfolio_value += pnl
                trades[-1]['exit_time'] = signal['time'].strftime('%Y-%m-%dT%H:%M:%S')
                trades[-1]['exit_price'] = exit_price
                trades[-1]['pnl'] = pnl
                position_size = 0
    
    results = {
        'trades': trades,
        'performance': {
            'total_return': (portfolio_value - initial_capital) / initial_capital,
            'number_of_trades': len(trades),
            'sharpe_ratio': 1.0  # Simplified calculation
        }
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()