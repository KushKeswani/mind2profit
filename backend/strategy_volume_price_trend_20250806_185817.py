"""
Generated Strategy: Volume Price Trend
Description: Buy on high volume price breakouts, sell on volume decline. Monitor volume spikes with price movements.
Generated: 2025-08-06 18:58:17
"""

import requests
import pandas as pd
import ta
import json
from datetime import datetime

# Set Alpaca API credentials
ALPACA_API_KEY = 'PK0F1YSWGZYNHF1VKOY5'
ALPACA_SECRET_KEY = 'ZauOD5S8S3uUNk4C9eJemAZiY8GQocMu5izxNWAB'

def get_historical_data(symbol, start_date, end_date):
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
        response = requests.get(base_url + 'stocks/v2/historic/prices', headers=headers, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json()['prices'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_indicators(df):
    try:
        df['volume'] = pd.to_numeric(df['volume'])
        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        
        # Calculate indicators
        df['ma20'] = df['close'].rolling(20).mean()
        df['ma50'] = df['close'].rolling(50).mean()
        df['avg_volume_20'] = df['volume'].rolling(20).mean()
        df['avg_volume_50'] = df['volume'].rolling(50).mean()
        df['volume_ratio'] = df['volume'] / df['avg_volume_20']
        
        return df
    except Exception as e:
        print(f"Error calculating indicators: {e}")
        return None

def generate_trades(df, initial_capital, risk_per_trade):
    try:
        trades = []
        position_size = 0
        ma_length = 20
        
        for i in range(len(df)):
            if i < ma_length:
                continue
                
            current_price = df.iloc[i]['close']
            current_volume = df.iloc[i]['volume']
            ma20 = df.iloc[i]['ma20']
            ma50 = df.iloc[i]['ma50']
            avg_volume_20 = df.iloc[i]['avg_volume_20']
            volume_ratio = df.iloc[i]['volume_ratio']
            
            # Position sizing based on risk management
            if position_size == 0:
                position_size = (initial_capital * risk_per_trade) / (current_price * 0.01)
            
            # Buy signal: Price breaks above MA20 with increasing volume
            if current_price > ma20 and volume_ratio > 1:
                if position_size > 0:
                    trades.append({
                        'timestamp': df.index[i],
                        'type': 'buy',
                        'price': current_price,
                        'quantity': position_size,
                        'value': position_size * current_price
                    })
            
            # Sell signal: Price breaks below MA50 with decreasing volume
            elif current_price < ma50 and volume_ratio < 1:
                if position_size > 0:
                    trades.append({
                        'timestamp': df.index[i],
                        'type': 'sell',
                        'price': current_price,
                        'quantity': position_size,
                        'value': position_size * current_price
                    })
        
        return trades
    except Exception as e:
        print(f"Error generating trades: {e}")
        return []

def main():
    try:
        symbol = 'QQQ'
        start_date = '2025-01-01'
        end_date = '2025-03-01'
        initial_capital = 100000
        risk_per_trade = 0.01
        
        # Fetch data
        df = get_historical_data(symbol, start_date, end_date)
        if df is None:
            return
        
        # Calculate indicators
        df = calculate_indicators(df)
        if df is None:
            return
        
        # Generate trades
        trades = generate_trades(df, initial_capital, risk_per_trade)
        
        # Calculate performance
        total_profit = sum([trade['value'] for trade in trades]) if trades else 0
        num_trades = len(trades)
        win_rate = sum([1 for trade in trades if trade['type'] == 'sell']) / num_trades if num_trades > 0 else 0
        
        # Create results dictionary
        results = {
            'trades': trades,
            'performance': {
                'total_profit': total_profit,
                'num_trades': num_trades,
                'win_rate': win_rate,
                'initial_capital': initial_capital
            }
        }
        
        # Export to JSON
        with open('backtest_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print("Backtest completed successfully!")
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()