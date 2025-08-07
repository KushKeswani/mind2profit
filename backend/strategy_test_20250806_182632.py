"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 18:26:32
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

def get_data(symbol, start_date, end_date, timeframe):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        api_key = 'PK0F1YSWGZYNHF1VKOY5'
        api_secret = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
        headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}
        
        start_date = start_date + 'T00:00:00'
        end_date = end_date + 'T23:59:59'
        
        params = {
            'symbol': symbol,
            'timeframe': timeframe,
            'start': start_date,
            'end': end_date,
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame([d['close'] for d in data], index=pd.to_datetime([d['timestamp'] for d in data]), columns=['close'])
        df = df.sort_index()
        
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(df, short_ma=20, long_ma=50):
    try:
        df['short_ma'] = df['close'].rolling(window=short_ma).mean()
        df['long_ma'] = df['close'].rolling(window=long_ma).mean()
        df['atr'] = ta.volatility.AverageTrueRange(df, window=14).average_true_range()
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def backtest_strategy(df, initial_capital=100000):
    try:
        df['signal'] = 0
        df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
        df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1
        
        df['position'] = df['signal'].diff()
        df['pnl'] = df['position'].shift(1) * (df['close'].diff())
        
        trades = []
        total_profit = 0
        num_trades = 0
        winning_trades = 0
        
        for i in range(1, len(df)):
            if df['position'].iloc[i] != 0:
                entry_price = df['close'].iloc[i-1]
                exit_price = df['close'].iloc[i]
                profit = (exit_price - entry_price) / entry_price
                total_profit += profit
                num_trades += 1
                if profit > 0:
                    winning_trades += 1
                trades.append({
                    'entry_time': str(df.index[i-1]),
                    'exit_time': str(df.index[i]),
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'profit': profit
                })
        
        performance = {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'winning_trades': winning_trades,
            'win_rate': winning_trades/num_trades if num_trades > 0 else 0,
            'trades': trades
        }
        
        return performance
    except Exception as e:
        print(f"Error running backtest: {e}")
        return None

def calculate_position_size(df, risk_percent=1.0):
    try:
        risk_amount = df['close'] * risk_percent / 100
        position_size = risk_amount / (df['atr'] * 2)
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        
        df = get_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return
            
        df = calculate_indicators(df)
        if df is None:
            return
            
        position_size = calculate_position_size(df)
        if position_size is None:
            return
            
        performance = backtest_strategy(df)
        if performance is None:
            return
            
        results = {
            'symbol': symbol,
            'timeframe': timeframe,
            'start_date': start_date,
            'end_date': end_date,
            'performance': performance
        }
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=4)
            
        print("Backtest completed successfully!")
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()