"""
Generated Strategy: test
Description: Simple moving average crossover
Generated: 2025-08-06 17:59:03
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

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

def calculate_indicators(df):
    try:
        df['short_ma'] = df['close'].rolling(20).mean()
        df['long_ma'] = df['close'].rolling(50).mean()
        df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=14)
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def generate_signals(df):
    try:
        signals = pd.DataFrame(index=df.index, columns=['signal'])
        signals['signal'] = 0
        signals.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
        signals.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1
        return signals
    except Exception as e:
        print(f"Error generating signals: {e}")
        return None

def calculate_position_size(account_balance, risk_percent, stop_loss):
    try:
        position_size = (account_balance * risk_percent) / stop_loss
        return position_size
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def backtest_strategy():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        timeframe = '1Min'
        risk_percent = 0.01
        
        df = get_alpaca_data(symbol, start_date, end_date, timeframe)
        if df is None:
            return
        
        df = calculate_indicators(df)
        if df is None:
            return
        
        signals = generate_signals(df)
        if signals is None:
            return
        
        trades = []
        position_size = 0
        account_balance = 100000  # Initial balance
        
        for i in range(len(df)):
            if signals.iloc[i]['signal'] == 1 and signals.iloc[i-1]['signal'] != 1:
                # Calculate position size
                stop_loss = df.iloc[i]['close'] - df.iloc[i]['low']
                position_size = calculate_position_size(account_balance, risk_percent, stop_loss)
                
                # Execute buy
                trades.append({
                    'type': 'buy',
                    'timestamp': df.index[i],
                    'price': df.iloc[i]['close'],
                    'size': position_size,
                    'stop_loss': df.iloc[i]['low']
                })
                
            elif signals.iloc[i]['signal'] == -1 and signals.iloc[i-1]['signal'] != -1:
                # Execute sell
                trades.append({
                    'type': 'sell',
                    'timestamp': df.index[i],
                    'price': df.iloc[i]['close'],
                    'size': position_size,
                    'stop_loss': df.iloc[i]['high']
                })
        
        # Calculate performance metrics
        total_trades = len(trades)
        profitable_trades = len([t for t in trades if t['type'] == 'sell' and t['price'] > t['stop_loss']])
        win_rate = profitable_trades / total_trades if total_trades > 0 else 0
        
        # Prepare results
        results = {
            'trades': trades,
            'performance': {
                'total_trades': total_trades,
                'win_rate': win_rate,
                'initial_balance': account_balance,
                'final_balance': account_balance  # Simplified, actual P&L calculation needed
            }
        }
        
        return results
    except Exception as e:
        print(f"Error in backtest_strategy: {e}")
        return None

def main():
    try:
        results = backtest_strategy()
        if results is not None:
            with open('backtest_results.json', 'w') as f:
                json.dump(results, f, indent=4, default=str)
            print("Backtest results exported to backtest_results.json")
        else:
            print("Backtest failed")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()