"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 14:51:39
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API credentials
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def get_data(symbol, start_date, end_date):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/stocks/' + symbol + '/bars'
        params = {
            'timeframe': '1Min',
            'start': start_date,
            'end': end_date,
            'limit': 1000
        }
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(df):
    try:
        df['volume_sma'] = ta.volatility.SimpleMovingAverage(df['volume'], 20)
        df['current_volume_ratio'] = df['volume'] / df['volume_sma']
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def strategy_logic(df):
    try:
        trades = []
        position = False
        for i in range(len(df)):
            current_row = df.iloc[i]
            prev_row = df.iloc[i-1] if i > 0 else None
            
            if prev_row is not None:
                if current_row['volume'] > current_row['volume_sma'] and current_row['close'] > prev_row['high']:
                    if not position:
                        position = True
                        trade_size = (0.01 * 100000) / current_row['close']
                        trades.append({
                            'type': 'buy',
                            'price': current_row['close'],
                            'volume': trade_size,
                            'value': trade_size * current_row['close'],
                            'timestamp': current_row['timestamp']
                        })
                elif current_row['volume'] < current_row['volume_sma'] and current_row['close'] < prev_row['low']:
                    if position:
                        position = False
                        trade_size = (0.01 * 100000) / current_row['close']
                        trades.append({
                            'type': 'sell',
                            'price': current_row['close'],
                            'volume': trade_size,
                            'value': trade_size * current_row['close'],
                            'timestamp': current_row['timestamp']
                        })
        return trades
    except Exception as e:
        print(f"Error executing strategy: {e}")
        return []

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        
        # Fetch data
        df = get_data(symbol, start_date, end_date)
        if df is None:
            return
            
        # Calculate indicators
        df = calculate_indicators(df)
        if df is None:
            return
            
        # Execute strategy
        trades = strategy_logic(df)
        
        # Calculate performance
        total_profit = sum(trade['value'] * (1 if trade['type'] == 'sell' else -1) for trade in trades)
        num_trades = len(trades)
        win_rate = sum(1 for trade in trades if trade['type'] == 'sell') / (num_trades / 2) if num_trades > 0 else 0
        
        # Format results
        results = {
            'trades': trades,
            'metrics': {
                'total_profit': total_profit,
                'num_trades': num_trades,
                'win_rate': win_rate
            }
        }
        
        # Export to JSON
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print("Backtest completed successfully!")
    except Exception as e:
        print(f"Main error: {e}")

if __name__ == "__main__":
    main()