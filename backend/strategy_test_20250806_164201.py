"""
Generated Strategy: Test
Description: Test strategy
Generated: 2025-08-06 16:42:01
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API keys
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def fetch_data(symbol, start_date, end_date):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
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
        
        response = requests.get(base_url + 'stocks/v2/pricebars/', headers=headers, params=params)
        if response.status_code == 200:
            return pd.json_normalize(response.json()['bars'])
        return None
    except Exception as e:
        print(f'Error fetching data: {e}')
        return None

def calculate_position_size(risk_amount, df):
    try:
        df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
        position_size = (risk_amount / df['ATR'].iloc[-1]) * 100  # Assuming 100 shares per $1
        return int(position_size)
    except Exception as e:
        print(f'Error calculating position size: {e}')
        return 0

def generate_trades(df):
    try:
        trades = []
        for i in range(1, len(df)):
            if df['close'].iloc[i] > df['close'].iloc[i-1]:
                # Generate buy signal
                trades.append({
                    'entry_time': df.index[i],
                    'entry_price': df['close'].iloc[i],
                    'exit_time': df.index[i+1],
                    'exit_price': df['close'].iloc[i+1],
                    'type': 'buy'
                })
        return trades
    except Exception as e:
        print(f'Error generating trades: {e}')
        return []

def calculate_performance(trades, initial_capital):
    try:
        total_profit = 0
        for trade in trades:
            profit = trade['exit_price'] - trade['entry_price']
            total_profit += profit
        
        num_trades = len(trades)
        if num_trades == 0:
            return {
                'total_profit': 0,
                'num_trades': 0,
                'sharpe_ratio': 0
            }
            
        average_profit = total_profit / num_trades
        sharpe_ratio = average_profit  # Simplified calculation
        return {
            'total_profit': total_profit,
            'num_trades': num_trades,
            'sharpe_ratio': sharpe_ratio
        }
    except Exception as e:
        print(f'Error calculating performance: {e}')
        return {
            'total_profit': 0,
            'num_trades': 0,
            'sharpe_ratio': 0
        }

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        risk_per_trade = 0.01
        initial_capital = 100000
        
        df = fetch_data(symbol, start_date, end_date)
        if df is None:
            print('Failed to fetch data')
            return
            
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        
        # Add technical indicators
        df['SMA_20'] = df['close'].rolling(20).mean()
        
        risk_amount = initial_capital * risk_per_trade
        position_size = calculate_position_size(risk_amount, df)
        
        trades = generate_trades(df)
        
        performance = calculate_performance(trades, initial_capital)
        
        # Format results
        results = {
            'symbol': symbol,
            'start_date': start_date,
            'end_date': end_date,
            'risk_per_trade': risk_per_trade,
            'initial_capital': initial_capital,
            'trades': trades,
            'performance': performance
        }
        
        # Export to JSON
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print('Backtest completed successfully')
        
    except Exception as e:
        print(f'Error in main function: {e}')

if __name__ == "__main__":
    main()