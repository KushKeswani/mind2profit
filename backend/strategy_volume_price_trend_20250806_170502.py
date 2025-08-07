"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 17:05:02
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API keys
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def get_historical_data(symbol, start_date, end_date):
    try:
        base_url = 'https://paper-api.alpaca.markets/v2/'
        endpoint = f'stocks/{symbol}/bars?timeframe=1Min&start={start_date}&end={end_date}'
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
        }
        response = requests.get(base_url + endpoint, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json()['bars'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(df):
    try:
        # Calculate volume moving averages
        df['vol_20'] = df['volume'].rolling(20).mean()
        df['vol_50'] = df['volume'].rolling(50).mean()
        
        # Calculate price change percentage
        df['price_change_pct'] = df['close'].pct_change() * 100
        
        # Calculate average true range
        df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
        
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def strategy_logic(df):
    try:
        trades = []
        position = None
        
        for i in range(len(df)):
            row = df.iloc[i]
            
            if position is None:
                # Buy condition: Price breaks above 20-period high with increasing volume
                if row['close'] > df.iloc[i-20]['high'].max() and row['volume'] > row['vol_20']:
                    position = {
                        'entry_price': row['close'],
                        'entry_time': row['timestamp'],
                        'size': calculate_position_size(row['close'])
                    }
                    trades.append({'type': 'buy', **position})
            
            else:
                # Sell condition: Price drops below 50-period low or price starts to decline
                if row['close'] < df.iloc[i-50]['low'].min() or row['price_change_pct'] < 0:
                    position['exit_price'] = row['close']
                    position['exit_time'] = row['timestamp']
                    position['pnl'] = position['exit_price'] - position['entry_price']
                    trades[-1] = position
                    position = None
        
        return trades
    except Exception as e:
        print(f"Error executing strategy: {e}")
        return []

def calculate_position_size(entry_price):
    try:
        # Risk 1% per trade
        risk_amount = 0.01 * 100000  # Assuming $100,000 account size
        stop_loss = entry_price * 0.02  # 2% stop loss
        position_size = risk_amount / stop_loss
        return int(position_size)
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0

def generate_results(trades):
    try:
        results = {
            'trades': trades,
            'total_profit': sum(t['pnl'] for t in trades if 'pnl' in t),
            'num_trades': len(trades),
            'win_rate': sum(1 for t in trades if t.get('pnl', 0) > 0) / len(trades) if trades else 0
        }
        return results
    except Exception as e:
        print(f"Error generating results: {e}")
        return {}

def export_to_json(results, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        return True
    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return False

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    
    df = get_historical_data(symbol, start_date, end_date)
    if df is not None:
        df = calculate_indicators(df)
        if df is not None:
            trades = strategy_logic(df)
            if trades:
                results = generate_results(trades)
                if export_to_json(results, 'backtest_results.json'):
                    print("Backtest completed successfully")
                else:
                    print("Failed to export results")
            else:
                print("No trades executed")
        else:
            print("Failed to calculate indicators")
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    main()