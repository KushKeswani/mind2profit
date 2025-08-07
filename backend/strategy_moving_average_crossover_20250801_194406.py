"""
Generated Strategy: Moving Average Crossover
Description: 
    Create a moving average crossover strategy for QQQ:
    - Use 20-period and 50-period simple moving averages
    - Buy when 20 SMA crosses above 50 SMA
    - Sell when 20 SMA crosses below 50 SMA
    - Use 1-minute data from January 2025 to March 2025
    - Include proper risk management and position sizing
    
Generated: 2025-08-01 19:44:06
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

# API Configuration
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

def fetch_data(symbol, start_date, end_date):
    try:
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': '1Minute',
            'limit': 10000
        }
        response = requests.get(f'{ALPACA_BASE_URL}/v2/data/bars', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['SMA_20'] = ta.momentum.SMAIndicator(df['close'], window=20).sma_indicator()
        df['SMA_50'] = ta.momentum.SMAIndicator(df['close'], window=50).sma_indicator()
        df['signal'] = 0
        df.loc[df['SMA_20'] > df['SMA_50'], 'signal'] = 1
        df.loc[df['SMA_20'] < df['SMA_50'], 'signal'] = -1
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def strategy_logic(df):
    try:
        df['position'] = df['signal'].diff()
        df['buy_signal'] = (df['position'] == 2)
        df['sell_signal'] = (df['position'] == -2)
        df['PNL'] = df['close'].pct_change().cumsum()
        df['max_drawdown'] = df['close'].expanding().max() - df['close']
        df['Sharpe_Ratio'] = df['close'].pct_change().mean() / df['close'].pct_change().std()
        df['win_rate'] = df['buy_signal'].rolling(20).mean()
        return df
    except Exception as e:
        print(f'Error in strategy logic: {e}')
        return None

def execute_trades(df):
    try:
        trades = []
        position_size = 10000  # Fixed position size
        for i in range(1, len(df)):
            if df.iloc[i-1]['buy_signal']:
                entry_price = df.iloc[i]['open']
                shares = position_size / entry_price
                trades.append({
                    'type': 'buy',
                    'entry_price': entry_price,
                    'shares': shares,
                    'entry_time': df.index[i]
                })
            elif df.iloc[i-1]['sell_signal']:
                if trades and trades[-1]['type'] == 'buy':
                    exit_price = df.iloc[i]['open']
                    profit = (exit_price - trades[-1]['entry_price']) * trades[-1]['shares']
                    duration = df.index[i] - trades[-1]['entry_time']
                    trades[-1]['exit_price'] = exit_price
                    trades[-1]['profit'] = profit
                    trades[-1]['exit_time'] = df.index[i]
                    trades[-1]['duration'] = duration
        return trades
    except Exception as e:
        print(f'Error executing trades: {e}')
        return None

def analyze_results(trades, df):
    try:
        total_profit = sum(t['profit'] for t in trades if 'profit' in t)
        max_drawdown = df['max_drawdown'].max()
        sharpe_ratio = df['Sharpe_Ratio'].mean()
        win_rate = df['win_rate'].mean()
        results = {
            'total_profit': total_profit,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'trades': trades
        }
        return results
    except Exception as e:
        print(f'Error analyzing results: {e}')
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        df = fetch_data(symbol, start_date, end_date)
        if df is None:
            return
            
        df = calculate_indicators(df)
        if df is None:
            return
            
        df = strategy_logic(df)
        if df is None:
            return
            
        trades = execute_trades(df)
        if trades is None:
            return
            
        results = analyze_results(trades, df)
        if results is None:
            return
        
        with open('strategy_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully')
    except Exception as e:
        print(f'Error in main execution: {e}')

if __name__ == '__main__':
    main()