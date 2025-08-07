"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 18:16:25
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
            'timeframe': timeframe
        }
        
        response = requests.get(base_url + 'stocks/' + symbol + '/bars', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_macd(df):
    try:
        df['macd'] = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).macd()
        df['signal'] = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9).signal()
        return df
    except Exception as e:
        print(f'Error calculating MACD: {e}')
        return None

def generate_signals(df):
    try:
        signals = []
        for i in range(1, len(df)):
            prev_macd = df['macd'].iloc[i-1]
            curr_macd = df['macd'].iloc[i]
            prev_signal = df['signal'].iloc[i-1]
            curr_signal = df['signal'].iloc[i]
            
            if curr_macd > curr_signal and prev_macd <= prev_signal:
                signals.append({'timestamp': df.index[i], 'type': 'buy'})
            elif curr_macd < curr_signal and prev_macd >= prev_signal:
                signals.append({'timestamp': df.index[i], 'type': 'sell'})
        return signals
    except Exception as e:
        print(f'Error generating signals: {e}')
        return None

def calculate_position_size(portfolio_value, risk_per_trade, current_price):
    try:
        risk_amount = portfolio_value * risk_per_trade
        position_size = risk_amount / current_price
        return position_size
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def backtest_strategy():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        initial_portfolio = 100000
        risk_per_trade = 0.01
        
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return None
            
        df = calculate_macd(df)
        if df is None:
            return None
            
        signals = generate_signals(df)
        if signals is None:
            return None
        
        trades = []
        portfolio_value = initial_portfolio
        position_size = 0
        current_price = 0
        
        for signal in signals:
            timestamp = signal['timestamp']
            if timestamp in df.index:
                current_price = df.loc[timestamp, 'close']
                position_size = calculate_position_size(portfolio_value, risk_per_trade, current_price)
                
                if signal['type'] == 'buy':
                    trades.append({
                        'timestamp': timestamp,
                        'type': 'buy',
                        'price': current_price,
                        'shares': position_size,
                        'value': position_size * current_price
                    })
                    portfolio_value += position_size * current_price
                else:
                    trades.append({
                        'timestamp': timestamp,
                        'type': 'sell',
                        'price': current_price,
                        'shares': position_size,
                        'value': -position_size * current_price
                    })
                    portfolio_value -= position_size * current_price
        
        performance = {
            'total_profit': portfolio_value - initial_portfolio,
            'number_of_trades': len(trades),
            'win_rate': sum(1 for trade in trades if trade['type'] == 'sell' and trade['value'] > 0) / len(trades) if trades else 0
        }
        
        results = {
            'trades': trades,
            'performance': performance
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        return results
    except Exception as e:
        print(f'Error in backtest strategy: {e}')
        return None

def main():
    results = backtest_strategy()
    if results:
        print('Backtest completed successfully')
    else:
        print('Backtest failed')

if __name__ == "__main__":
    main()