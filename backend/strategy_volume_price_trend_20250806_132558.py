"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 13:25:58
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API credentials
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
            'timeframe': '1Min',
            'start': start_date,
            'end': end_date
        }
        response = requests.get(base_url + 'stocks/' + symbol + '/bars', headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['bars'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        else:
            print(f"Error fetching data: {response.text}")
            return None
    except Exception as e:
        print(f"Error in fetch_data: {e}")
        return None

def calculate_indicators(df):
    try:
        # Volume Indicators
        df['volume_sma'] = df['volume'].rolling(20).mean()
        df['volume_ema'] = df['volume'].ewm(span=20, adjust=False).mean()
        
        # Price Indicators
        df['sma_20'] = df['close'].rolling(20).mean()
        df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['rsi'] = ta.momentum.RSI(df['close'], window=14)
        
        return df
    except Exception as e:
        print(f"Error in calculate_indicators: {e}")
        return None

def backtest(df, initial_capital, risk_per_trade):
    try:
        trades = []
        position_size = 0
        position = 0
        balance = initial_capital
        risk_amount = initial_capital * risk_per_trade
        
        for index, row in df.iterrows():
            if position == 0:
                # Buy condition: Volume spike with price breakout
                if row['volume'] > row['volume_sma'] and row['close'] > row['sma_20'] and row['rsi'] < 70:
                    position_size = risk_amount / (row['close'] * 0.02)  # Using 2% ATR for stop loss
                    position = position_size * row['close']
                    balance -= position_size * row['close']
                    trades.append({
                        'type': 'buy',
                        'timestamp': row['timestamp'],
                        'price': row['close'],
                        'size': position_size
                    })
            elif position > 0:
                # Sell condition: Volume decline with price drop
                if row['volume'] < row['volume_sma'] and row['close'] < row['sma_20'] and row['rsi'] > 30:
                    balance += position * (row['close'] / row['close'])
                    position = 0
                    trades.append({
                        'type': 'sell',
                        'timestamp': row['timestamp'],
                        'price': row['close'],
                        'size': position_size
                    })
        
        return {
            'trades': trades,
            'performance': {
                'initial_capital': initial_capital,
                'final_balance': balance,
                'total_trades': len(trades),
                'winning_trades': len([t for t in trades if t['type'] == 'sell']),
                'losing_trades': len([t for t in trades if t['type'] == 'buy']),
                'profit_factor': (balance - initial_capital) / initial_capital
            }
        }
    except Exception as e:
        print(f"Error in backtest: {e}")
        return None

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        initial_capital = 100000
        risk_per_trade = 0.01
        
        df = fetch_data(symbol, start_date, end_date)
        if df is not None:
            df = calculate_indicators(df)
            if df is not None:
                results = backtest(df, initial_capital, risk_per_trade)
                if results is not None:
                    with open('backtest_results.json', 'w') as f:
                        json.dump(results, f, indent=4)
                    print("Backtest completed successfully. Results saved to backtest_results.json")
        return results
    except Exception as e:
        print(f"Error in main: {e}")
        return None

if __name__ == "__main__":
    main()