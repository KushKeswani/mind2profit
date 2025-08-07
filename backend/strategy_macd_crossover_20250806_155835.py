"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 15:58:35
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
    df['MACD'], df['MACD_Signal'] = ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).macd(), ta.momentum.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).macd_signal()
    return df

def generate_signals(df):
    df['Signal'] = 0
    df.loc[df['MACD'] > df['MACD_Signal'], 'Signal'] = 1
    df.loc[df['MACD'] < df['MACD_Signal'], 'Signal'] = -1
    return df

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
    df = generate_signals(df)
    
    trades = []
    portfolio_value = initial_capital
    position_size = 0
    
    for i in range(1, len(df)):
        current_row = df.iloc[i]
        previous_row = df.iloc[i-1]
        
        if previous_row['Signal'] == 1 and current_row['Signal'] == 1:
            if position_size == 0:
                entry_price = current_row['close']
                position_size = calculate_position_size(portfolio_value, risk_per_trade, entry_price)
                trades.append({
                    'type': 'buy',
                    'entry_price': entry_price,
                    'entry_time': current_row.name
                })
        
        elif previous_row['Signal'] == -1 and current_row['Signal'] == -1:
            if position_size > 0:
                exit_price = current_row['close']
                pnl = (exit_price - trades[-1]['entry_price']) * position_size
                portfolio_value += pnl
                trades[-1]['exit_price'] = exit_price
                trades[-1]['exit_time'] = current_row.name
                trades[-1]['pnl'] = pnl
                position_size = 0
    
    results = {
        'trades': trades,
        'final_portfolio_value': portfolio_value,
        'total_trades': len(trades),
        'winning_trades': sum(1 for trade in trades if trade.get('pnl', 0) > 0),
        'losing_trades': sum(1 for trade in trades if trade.get('pnl', 0) < 0),
        'win_rate': (sum(1 for trade in trades if trade.get('pnl', 0) > 0) / len(trades)) if len(trades) > 0 else 0
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