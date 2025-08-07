"""
Generated Strategy: MACD Crossover
Description: Buy when MACD line crosses above signal line, sell when it crosses below. Use standard 12,26,9 parameters.
Generated: 2025-08-06 16:16:50
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
        
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = (end_date + timedelta(days=1)).strftime('%Y-%m-%d')
        
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': timeframe,
            'limit': 10000
        }
        
        response = requests.get(base_url + 'stocks/v2/minute', headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data['minute'])
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_macd(df):
    try:
        macd = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd.macd()
        df['signal'] = macd.signal()
        return df
    except Exception as e:
        print(f'Error calculating MACD: {e}')
        return None

def backtest_strategy(df, initial_equity, risk_per_trade):
    try:
        trades = []
        position_size = 0
        equity = initial_equity
        macd_prev = None
        signal_prev = None
        
        for index, row in df.iterrows():
            if macd_prev is not None and signal_prev is not None:
                # Check for crossover
                if row['macd'] > row['signal'] and macd_prev < signal_prev:
                    # Buy signal
                    if position_size == 0:
                        # Calculate position size based on risk
                        position_size = int((equity * risk_per_trade) / row['close'])
                        if position_size > 0:
                            trades.append({
                                'type': 'buy',
                                'time': index.strftime('%Y-%m-%dT%H:%M:%S'),
                                'price': row['close'],
                                'shares': position_size,
                                'equity': equity
                            })
                elif row['macd'] < row['signal'] and macd_prev > signal_prev:
                    # Sell signal
                    if position_size > 0:
                        profit = (row['close'] - trades[-1]['price']) * position_size
                        equity += profit
                        trades.append({
                            'type': 'sell',
                            'time': index.strftime('%Y-%m-%dT%H:%M:%S'),
                            'price': row['close'],
                            'shares': position_size,
                            'equity': equity
                        })
                        position_size = 0
            macd_prev = row['macd']
            signal_prev = row['signal']
            
        return trades
    except Exception as e:
        print(f'Error executing strategy: {e}')
        return []

def calculate_performance(trades, initial_equity):
    try:
        total_profit = sum(t['price'] * t['shares'] * (-1 if t['type'] == 'buy' else 1) for t in trades)
        num_trades = len(trades)
        if num_trades == 0:
            return {'total_profit': 0, 'num_trades': 0, 'sharpe_ratio': 0}
        
        returns = []
        for i in range(1, len(trades)):
            if trades[i-1]['type'] == 'buy' and trades[i]['type'] == 'sell':
                profit = trades[i]['equity'] - trades[i-1]['equity']
                returns.append(profit / initial_equity)
        
        if len(returns) == 0:
            return {'total_profit': total_profit, 'num_trades': num_trades, 'sharpe_ratio': 0}
        
        sharpe_ratio = (sum(returns) / len(returns)) / (std_dev(returns) * (len(returns) ** 0.5))
        return {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'sharpe_ratio': sharpe_ratio
        }
    except Exception as e:
        print(f'Error calculating performance: {e}')
        return {'total_profit': 0, 'num_trades': 0, 'sharpe_ratio': 0}

def std_dev(returns):
    mean = sum(returns) / len(returns)
    squared_diffs = [(x - mean) ** 2 for x in returns]
    return (sum(squared_diffs) / len(returns)) ** 0.5

def main():
    symbol = 'QQQ'
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 3, 1)
    timeframe = '1Min'
    initial_equity = 100000
    risk_per_trade = 0.01
    
    df = get_alpaca_data(symbol, start_date, end_date, timeframe)
    if df is not None:
        df = calculate_macd(df)
        if 'macd' in df.columns:
            trades = backtest_strategy(df, initial_equity, risk_per_trade)
            performance = calculate_performance(trades, initial_equity)
            
            results = {
                'trades': trades,
                'performance': {
                    'total_profit': performance['total_profit'],
                    'num_trades': performance['num_trades'],
                    'sharpe_ratio': performance['sharpe_ratio']
                }
            }
            
            with open('backtest_results.json', 'w') as f:
                json.dump(results, f, indent=2)
                
            print('Backtest completed successfully')
        else:
            print('Failed to calculate MACD')
    else:
        print('Failed to fetch data')

if __name__ == "__main__":
    main()