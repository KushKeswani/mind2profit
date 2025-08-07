"""
Generated Strategy: Moving Average Crossover
Description: 
    Create a moving average crossover strategy for QQQ:
    - Use 20-period and 50-period simple moving averages
    - Buy when 20 SMA crosses above 50 SMA
    - Sell when 20 SMA crosses below 50 SMA
    - Use 1-minute data from January 2025 to March 2025
    - Include proper risk management and position sizing
    
Generated: 2025-08-01 19:47:23
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

# Configure Alpaca API
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

def fetch_data(symbol, start_date, end_date):
    try:
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        url = f'{ALPACA_BASE_URL}/v2/data/minute/{symbol}'
        params = {
            'start': start_date,
            'end': end_date,
            'limit': 10000
        }
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['minute'])
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['sma_20'] = ta.momentum.SMA(df['close'], window=20).SMA()
        df['sma_50'] = ta.momentum.SMA(df['close'], window=50).SMA()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def strategy_logic(df):
    try:
        signals = []
        for i in range(len(df)):
            if df['sma_20'].iloc[i] > df['sma_50'].iloc[i] and df['sma_20'].iloc[i-1] <= df['sma_50'].iloc[i-1]:
                signals.append(('buy', df.index[i], df['close'].iloc[i]))
            elif df['sma_20'].iloc[i] < df['sma_50'].iloc[i] and df['sma_20'].iloc[i-1] >= df['sma_50'].iloc[i-1]:
                signals.append(('sell', df.index[i], df['close'].iloc[i]))
        return signals
    except Exception as e:
        print(f'Error in strategy logic: {e}')
        return None

def execute_trades(signals, initial_capital):
    try:
        trades = []
        position_size = 0
        position_value = 0
        portfolio_value = initial_capital
        for signal in signals:
            action, timestamp, price = signal
            if action == 'buy':
                if position_size == 0:
                    position_size = portfolio_value / price
                    position_value = position_size * price
                    trades.append({
                        'type': 'buy',
                        'entry_time': timestamp.isoformat(),
                        'entry_price': price,
                        'position_size': position_size,
                        'position_value': position_value
                    })
            elif action == 'sell':
                if position_size > 0:
                    profit = position_size * (price - position_value / position_size)
                    portfolio_value += profit - 1  # Subtract $1 commission
                    duration = (timestamp - trades[-1]['entry_time']).total_seconds() / 60
                    trades[-1]['exit_time'] = timestamp.isoformat()
                    trades[-1]['exit_price'] = price
                    trades[-1]['profit'] = profit
                    trades[-1]['duration'] = duration
                    position_size = 0
                    position_value = 0
        return trades
    except Exception as e:
        print(f'Error executing trades: {e}')
        return None

def analyze_results(trades):
    try:
        total_profit = sum(t['profit'] for t in trades if 'profit' in t)
        num_trades = len([t for t in trades if 'profit' in t])
        win_rate = sum(1 for t in trades if t.get('profit', 0) > 0) / num_trades if num_trades > 0 else 0
        results = {
            'total_profit': total_profit,
            'num_trades': num_trades,
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
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)
        
        df = fetch_data(symbol, start_date, end_date)
        if df is None:
            return
        
        df = calculate_indicators(df)
        if df is None:
            return
        
        signals = strategy_logic(df)
        if signals is None:
            return
        
        initial_capital = 100000
        trades = execute_trades(signals, initial_capital)
        if trades is None:
            return
        
        results = analyze_results(trades)
        if results is None:
            return
        
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully')
    except Exception as e:
        print(f'Error in main execution: {e}')

if __name__ == '__main__':
    main()