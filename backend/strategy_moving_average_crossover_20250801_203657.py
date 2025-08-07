"""
Generated Strategy: Moving Average Crossover
Description: Buy when short SMA crosses above long SMA, sell when it crosses below. Use 20-period and 50-period simple moving averages.
Generated: 2025-08-01 20:36:57
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
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'timeframe': '1Min',
            'limit': 10000
        }
        response = requests.get(f'{ALPACA_BASE_URL}/v2/data', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_indicators(df):
    try:
        df['sma_20'] = ta.momentum.SMAIndicator(df['close']).sma_indicator()
        df['sma_50'] = ta.momentum.SMAIndicator(df['close'], window=50).sma_indicator()
        return df
    except Exception as e:
        print(f'Error calculating indicators: {e}')
        return None

def strategy_logic(df):
    try:
        trades = []
        for i in range(len(df)):
            if i < 50:
                continue
            current = df.iloc[i]
            prev = df.iloc[i-1]
            
            if current['sma_20'] > current['sma_50'] and prev['sma_20'] <= prev['sma_50']:
                trades.append({
                    'symbol': 'QQQ',
                    'timestamp': current.name.isoformat(),
                    'type': 'buy',
                    'price': current['close'],
                    'performance': None
                })
            elif current['sma_20'] < current['sma_50'] and prev['sma_20'] >= prev['sma_50']:
                trades.append({
                    'symbol': 'QQQ',
                    'timestamp': current.name.isoformat(),
                    'type': 'sell',
                    'price': current['close'],
                    'performance': None
                })
        return trades
    except Exception as e:
        print(f'Error in strategy logic: {e}')
        return None

def execute_trades(trades):
    try:
        portfolio_value = 100000
        shares = 0
        trade_results = []
        for trade in trades:
            if trade['type'] == 'buy':
                shares = portfolio_value / trade['price']
                portfolio_value -= shares * trade['price']
            else:
                portfolio_value += shares * trade['price']
                shares = 0
            trade_results.append({
                'symbol': trade['symbol'],
                'timestamp': trade['timestamp'],
                'type': trade['type'],
                'price': trade['price'],
                'shares': shares if trade['type'] == 'buy' else -shares,
                'portfolio_value': portfolio_value
            })
        return trade_results
    except Exception as e:
        print(f'Error executing trades: {e}')
        return None

def analyze_results(trade_results):
    try:
        total_profit = sum(trade['price'] * trade['shares'] for trade in trade_results)
        num_trades = len(trade_results)
        wins = sum(1 for trade in trade_results if trade['type'] == 'sell' and trade['price'] > trade_results[trade_results.index(trade)-1]['price'])
        win_rate = wins / (num_trades // 2) if num_trades > 0 else 0
        return {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'win_rate': win_rate
        }
    except Exception as e:
        print(f'Error analyzing results: {e}')
        return None

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    
    df = fetch_data(symbol, start_date, end_date)
    if df is None:
        return
    
    df = calculate_indicators(df)
    if df is None:
        return
    
    trades = strategy_logic(df)
    if trades is None:
        return
    
    trade_results = execute_trades(trades)
    if trade_results is None:
        return
    
    results = analyze_results(trade_results)
    
    # Export results to JSON
    output = {
        'trade_list': trade_results,
        'performance': results
    }
    
    with open('backtest_results.json', 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    main()