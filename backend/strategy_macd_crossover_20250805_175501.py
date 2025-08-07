"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-05 17:55:01
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

def get_data(symbol, start_date, end_date, timeframe):
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
        
        response = requests.get(base_url + 'stocks/v2/intraday', params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_macd(df):
    try:
        macd = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd.macd()
        df['signal'] = macd.signal()
        return df
    except Exception as e:
        print(f"Error calculating MACD: {e}")
        return None

def backtest_strategy(df, risk_per_trade):
    try:
        trades = []
        position = 'flat'
        equity = 10000
        risk_amount = equity * risk_per_trade
        
        for i in range(1, len(df)):
            current_row = df.iloc[i]
            prev_row = df.iloc[i-1]
            
            if position == 'flat':
                if current_row['macd'] > current_row['signal'] and prev_row['macd'] < prev_row['signal']:
                    # Buy signal
                    position = 'long'
                    stop_loss = current_row['low'] - (current_row['high'] - current_row['low']) * 0.1
                    quantity = (risk_amount / (current_row['close'] - stop_loss)) * 0.95
                    trades.append({
                        'type': 'buy',
                        'timestamp': current_row.name.isoformat(),
                        'price': current_row['close'],
                        'quantity': quantity,
                        'stop_loss': stop_loss
                    })
            elif position == 'long':
                if current_row['macd'] < current_row['signal'] and prev_row['macd'] > prev_row['signal']:
                    # Sell signal
                    position = 'flat'
                    trades.append({
                        'type': 'sell',
                        'timestamp': current_row.name.isoformat(),
                        'price': current_row['close'],
                        'quantity': quantity,
                        'stop_loss': stop_loss
                    })
        
        return trades
    except Exception as e:
        print(f"Error in backtest strategy: {e}")
        return []

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        risk_per_trade = 0.01
        
        df = get_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return
            
        df = calculate_macd(df)
        if df is None:
            return
            
        trades = backtest_strategy(df, risk_per_trade)
        
        # Calculate performance metrics
        if not trades:
            print("No trades executed")
            return
            
        total_profit = sum((trade['sell']['price'] - trade['buy']['price']) * trade['buy']['quantity'] for trade in trades)
        max_drawdown = 0
        sharpe_ratio = 0
        
        # Create results dictionary
        results = {
            'trades': trades,
            'performance': {
                'total_profit': total_profit,
                'max_drawdown': max_drawdown,
                'sharpe_ratio': sharpe_ratio,
                'risk_per_trade': risk_per_trade
            },
            'parameters': {
                'symbol': symbol,
                'timeframe': timeframe,
                'start_date': start_date,
                'end_date': end_date
            }
        }
        
        # Export to JSON
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print("Backtest completed successfully")
        
    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()