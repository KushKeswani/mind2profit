"""
Generated Strategy: Bollinger Bands Strategy
Description: Buy when price touches lower band, sell when it reaches middle band. Use 20-period with 2 standard deviations.
Generated: 2025-08-06 13:38:15
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
        data = response.json()
        df = pd.DataFrame([x['price'] for x in data['prices']], columns=['price'])
        df.index = pd.to_datetime([x['timestamp'] for x in data['prices']])
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_bollinger_bands(df, period=20, std_dev=2):
    try:
        df['close'] = pd.to_numeric(df['price'])
        df['bb_middle'] = df['close'].rolling(window=period).mean()
        df['bb_std'] = df['close'].rolling(window=period).std()
        df['bb_lower'] = df['bb_middle'] - std_dev * df['bb_std']
        df['bb_upper'] = df['bb_middle'] + std_dev * df['bb_std']
        return df
    except Exception as e:
        print(f"Error calculating Bollinger Bands: {e}")
        return None

def backtest_strategy(df):
    try:
        trades = []
        position = None
        risk_per_trade = 0.01
        initial_capital = 100000  # Assuming initial capital for position sizing
        
        for i in range(len(df)):
            if i < 20:  # Wait for enough data to calculate BB
                continue
                
            close_price = df['close'].iloc[i]
            lower_band = df['bb_lower'].iloc[i]
            middle_band = df['bb_middle'].iloc[i]
            
            if position is None and close_price <= lower_band:
                # Buy signal
                position = close_price
                # Calculate position size based on risk management
                stop_loss = lower_band - close_price
                position_size = (initial_capital * risk_per_trade) / abs(stop_loss)
                trades.append({
                    'type': 'buy',
                    'price': close_price,
                    'timestamp': df.index[i],
                    'position_size': position_size
                })
                
            elif position is not None and close_price >= middle_band:
                # Sell signal
                profit = close_price - position
                position = None
                trades.append({
                    'type': 'sell',
                    'price': close_price,
                    'timestamp': df.index[i],
                    'profit': profit
                })
                
        return trades
    except Exception as e:
        print(f"Error executing strategy: {e}")
        return []

def export_results(trades, filename='backtest_results.json'):
    try:
        total_profit = sum(t['profit'] for t in trades if t['type'] == 'sell')
        num_trades = len(trades)
        results = {
            'trades': trades,
            'total_profit': total_profit,
            'num_trades': num_trades
        }
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        return True
    except Exception as e:
        print(f"Error exporting results: {e}")
        return False

def main():
    symbol = 'QQQ'
    start_date = '2025-01-01'
    end_date = '2025-03-01'
    
    df = get_historical_data(symbol, start_date, end_date)
    if df is not None:
        df = calculate_bollinger_bands(df)
        if df is not None:
            trades = backtest_strategy(df)
            if trades:
                export_results(trades)
                print("Backtest completed successfully")
            else:
                print("No trades executed")
        else:
            print("Failed to calculate Bollinger Bands")
    else:
        print("Failed to fetch historical data")

if __name__ == "__main__":
    main()