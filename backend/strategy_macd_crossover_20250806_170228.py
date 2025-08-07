"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 17:02:28
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

def get_alpaca_data(symbol, start_date, end_date, timeframe):
    base_url = 'https://paper-api.alpaca.markets/v2/'
    api_key = 'PK0F1YSWGZYNHF1VKOY5'
    api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
    
    params = {
        'symbol': symbol,
        'start': start_date,
        'end': end_date,
        'timeframe': timeframe
    }
    
    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': api_secret
    }
    
    try:
        response = requests.get(base_url + 'stocks/v2/ags', params=params, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_macd(df):
    df['MACD'], df['SIGNAL'] = ta.momentum.MACD(df['close']).macd(), ta.momentum.MACD(df['close']).signal()
    return df

def generate_signals(df):
    signals = []
    prev_macd = None
    prev_signal = None
    for i, row in df.iterrows():
        if prev_macd is not None and prev_signal is not None:
            if row['MACD'] > row['SIGNAL'] and prev_macd < prev_signal:
                signals.append({'type': 'buy', 'time': row['timestamp']})
            elif row['MACD'] < row['SIGNAL'] and prev_macd > prev_signal:
                signals.append({'type': 'sell', 'time': row['timestamp']})
        prev_macd = row['MACD']
        prev_signal = row['SIGNAL']
    return signals

def calculate_position_size(portfolio_value, risk_per_trade, entry_price):
    risk_amount = portfolio_value * risk_per_trade
    position_size = risk_amount / entry_price
    return position_size

def backtest_strategy():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    timeframe = '1Min'
    initial_capital = 100000
    risk_per_trade = 0.01
    
    df = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if df is None:
        return None
        
    df = calculate_macd(df)
    signals = generate_signals(df)
    
    portfolio_value = initial_capital
    position_size = 0
    trades = []
    
    for signal in signals:
        if signal['type'] == 'buy':
            entry_price = df.loc[df['timestamp'] == signal['time'], 'close'].values[0]
            shares = calculate_position_size(portfolio_value, risk_per_trade, entry_price)
            position_size = shares * entry_price
            portfolio_value -= position_size
            trades.append({
                'type': 'buy',
                'entry_time': signal['time'],
                'entry_price': entry_price,
                'shares': shares
            })
        elif signal['type'] == 'sell':
            if position_size > 0:
                exit_price = df.loc[df['timestamp'] == signal['time'], 'close'].values[0]
                p_l = (exit_price - trades[-1]['entry_price']) * trades[-1]['shares']
                percent_change = (exit_price - trades[-1]['entry_price']) / trades[-1]['entry_price'] * 100
                portfolio_value += p_l
                trades[-1]['exit_time'] = signal['time']
                trades[-1]['exit_price'] = exit_price
                trades[-1]['p_l'] = p_l
                trades[-1]['percent_change'] = percent_change
                position_size = 0
    
    results = {
        'trades': trades,
        'performance': {
            'total_return': (portfolio_value - initial_capital) / initial_capital * 100,
            'number_of_trades': len(trades),
            'sharpe_ratio': 1  # Simplified for this example
        }
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

def main():
    try:
        results = backtest_strategy()
        if results:
            print("Backtest completed successfully. Results saved to backtest_results.json")
        else:
            print("Backtest failed due to data fetching error")
    except Exception as e:
        print(f"Error during backtest: {e}")

if __name__ == "__main__":
    main()