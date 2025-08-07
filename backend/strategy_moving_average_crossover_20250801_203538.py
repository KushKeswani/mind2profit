"""
Generated Strategy: Moving Average Crossover
Description: Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.
Generated: 2025-08-01 20:35:38
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime, timedelta

# Configure Alpaca API
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'
API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
API_SECRET = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def fetch_data(symbol, start_date, end_date):
    """Fetch 1-minute data from Alpaca API"""
    try:
        headers = {
            'APCA-API-KEY-ID': API_KEY,
            'APCA-API-SECRET-KEY': API_SECRET
        }
        params = {
            'symbol': symbol,
            'timeframe': '1Min',
            'start': start_date,
            'end': end_date
        }
        response = requests.get(f'{ALPACA_BASE_URL}/v2/data/{symbol}/bars/1min', params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['bars'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(df):
    """Calculate 20-period and 50-period simple moving averages"""
    try:
        df['sma_20'] = ta.moving_average(df['close'], window=20)
        df['sma_50'] = ta.moving_average(df['close'], window=50)
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def strategy_logic(df):
    """Implement moving average crossover strategy"""
    try:
        trades = []
        position = 'flat'
        for i in range(len(df)):
            if df['sma_20'].iloc[i] > df['sma_50'].iloc[i] and position == 'flat':
                # Buy signal
                position = 'long'
                entry_price = df['close'].iloc[i]
                entry_time = df.index[i]
                trades.append({'type': 'buy', 'entry_time': entry_time, 'entry_price': entry_price})
            elif df['sma_20'].iloc[i] < df['sma_50'].iloc[i] and position == 'long':
                # Sell signal
                position = 'flat'
                exit_price = df['close'].iloc[i]
                exit_time = df.index[i]
                profit = exit_price - entry_price
                trades[-1]['exit_time'] = exit_time
                trades[-1]['exit_price'] = exit_price
                trades[-1]['profit'] = profit
        return trades
    except Exception as e:
        print(f"Error executing strategy: {e}")
        return None

def analyze_results(trades, df):
    """Analyze trading results"""
    try:
        if not trades:
            return None
        total_profit = sum(t['profit'] for t in trades)
        num_trades = len(trades)
        avg_profit = total_profit / num_trades if num_trades > 0 else 0
        max_drawdown = 0
        current_drawdown = 0
        for i in range(1, len(trades)):
            current_drawdown += trades[i]['profit']
            if current_drawdown < max_drawdown:
                max_drawdown = current_drawdown
        sharpe_ratio = (avg_profit / abs(max_drawdown)) if max_drawdown != 0 else 0
        return {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'avg_profit': avg_profit,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio
        }
    except Exception as e:
        print(f"Error analyzing results: {e}")
        return None

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    
    # Fetch data
    df = fetch_data(symbol, start_date, end_date)
    if df is None:
        return
    
    # Calculate indicators
    df = calculate_indicators(df)
    if df is None:
        return
    
    # Execute strategy
    trades = strategy_logic(df)
    if trades is None:
        return
    
    # Analyze results
    results = analyze_results(trades, df)
    if results is None:
        return
    
    # Export results to JSON
    with open('trades.json', 'w') as f:
        json.dump(trades, default=str, fp=f)
    
    with open('results.json', 'w') as f:
        json.dump(results, default=str, fp=f)

if __name__ == '__main__':
    main()